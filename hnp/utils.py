from hnp.client import Client
from natsort import natsorted


class ProjectListChoices(object):

    def __init__(self, token, project_id=None):
        self.token = token
        self.client = Client(token=token, project_id=project_id)
        self.project_list = self.client.get_list_projects()
        if project_id is not None:
            self.project = self.client.get_project()

    def get_choices(self):
        items = list()
        for item in self.project_list:
            items.append((list(item).pop(), item.get(list(item).pop()).get('name')))
        items = [('', '----')] + items
        return tuple(items)

    def get_houses(self):
        if self.project.get('houses'):
            return natsorted(self.project.get('houses'), key=lambda item: item.get('build_id'))
        else:
            return None

    def get_house_by_id(self, ids=list()):
        _houses = self.get_houses()
        houses = list()
        for house in _houses:
            if str(house.get('id')) in ids:
                houses.append(house)
        return houses


    def get_housetypes(self):
        return list(set([(lambda house: house.get('housetype'))(house) for house in self.project.get('houses')]))

    def get_project(self):
        return self.project
