from django.utils.translation import ugettext as _
from django.core.cache import cache
from hashlib import sha1

import requests
import json


def _update_keys(dictionary):
    new = {}
    if isinstance(dictionary, str):
        if dictionary.find('-') > 0:
            dictionary.replace('-', '_')
        return dictionary
    else:
        for k, v in dictionary.items():
            if isinstance(v, dict):
                v = _update_keys(v)
            elif isinstance(v, list) and v is not None:
                for vk, vv in enumerate(v):
                    v[vk] = _update_keys(vv)
            if k.find('-') > 0:
                new[k.replace('-', '_')] = v
            else:
                new[k] = v
    return new


class ApiRequestException(Exception):
    def __init__(self, status_code):
        message = "{0} gave http status: {1}".format(env('NIKI_API_URL'), status_code)
        super().__init__(message)


class CreateApiRequest(object):
    def __init__(self, token):
        self.api_url = env('NIKI_API_URL')
        self.token = token

    def get(self, resource='', *args, **kwargs):
        try:
            request_url = "{0}{1}?oauth_token{2}".format(self.api_url, resource, self.token)
            req_hash = sha1(request_url.encode()).hexdigest()
            if cache.get(req_hash) is None:
                req = requests.get("{0}/{1}".format(self.api_url, resource, args, kwargs),
                                   params={'oauth_token': self.token, 'phase': 'SALE'})
                json_response = ''
                if req.status_code != 200:
                    raise ApiRequestException(req.status_code)
                else:
                    if resource == '/about/version':
                        json_response = json.dumps({"version": req.text})
                    json_response = req.json()
                cache.set(req_hash, json_response, 3600)
            return cache.get(req_hash)

        except requests.exceptions.RequestException as e:
            import sys
            print(_("Connection error: %(exception)s" % {'exception': e}))
            sys.exit(1)


class Client(object):

    def __init__(self, token, project_id=None):
        self.project_id = project_id

        self._api_request = CreateApiRequest(token=token)

        self.projects = []
        self.house_types = []
        self.houses = []
        self.details = []

    def get_list_projects(self):
        """get a list of projects"""
        if not self.projects:
            try:
                response = self._api_request.get("/projects/mine")
                for project in response:
                    prj_id = project.get('id')
                    status = self._api_request.get(project.get('link')).get('status')
                    if status != 'Verkocht':
                        self.projects.append({prj_id: {'name': project['name'], 'link': project['link']}})
            except ValueError:
                self.projects = []

        return self.projects

    def _build_details(self, project_id=None):
        """build the project details"""
        if project_id is not None:
            self.project_id = project_id
        if self.project_id is None and project_id is None:
            raise AttributeError(_("Missing value for project_id"))
        _project_list = self.get_list_projects()
        projects = [(lambda x: list(x).pop())(x) for x in _project_list]
        index = projects.index(self.project_id)
        project_dict = [(lambda x: list(x.values()))(x) for x in _project_list][index].pop()
        project = self._api_request.get(project_dict.get('link'))

        '''build the project involved parties (brokers)'''
        parties_link = project.get('brokers.link')
        parties = self._api_request.get(parties_link)
        project['involved_parties'] = parties
        del project['involvedparties.link']

        '''buid the project housetypes'''
        housetypes_link = project.get('housetypes.link')
        housetypes = self._api_request.get(housetypes_link)
        project['housetypes'] = housetypes
        del project['housetypes.link']

        if project.get('housetypes'):
            '''build the project houses'''
            _houses = []
            _projects = []
            for link in [ht.get('self.link') for ht in project.get('housetypes')]:
                house = self._api_request.get(link)
                if house.get('houses'):
                    house_c = house['houses']
                    house['houses'] = list()
                    for hc in house_c:
                        if hc.get('status') != 'Verkocht':
                            hc = _update_keys(hc)
                            hc['housetype'] = house.get('name').lower().replace(' ', '-')
                            # DONT FORGET HACK TODO
                            house['houses'].append(hc)
                    _projects.append(house)

            for project in _projects:
                for houses in project.get('houses'):
                    _houses.append(houses)

            if _houses:
                project['houses'] = _houses

        return project

    def get_project(self, project_id=None):
        return self._build_details(project_id=project_id)
