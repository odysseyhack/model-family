from time import time
import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.views.generic import View
from oauthlib.oauth1 import rfc5849
from requests_oauthlib import OAuth1Session

from enrollment.settings import env
from hackathon.models import HNPOAuth
from hnp.client import CreateApiRequest, ApiRequestException



class RequestTokenView(View):

    def __init__(self):
        super().__init__()
        self.client_key = ''
        self.client_secret = ''
        self.oauth = ''
        self.resource_owner_key = ''
        self.resource_owner_secret = ''

    def get(self, request, pk):
        request.session['referrer'] = request.META.get('HTTP_REFERER')
        hnp_oauth = HNPOAuth.objects.get(pk=pk)
        self.client_key = hnp_oauth.client_name
        self.client_secret = 'IMPLEMENT_SECRET'

        self.oauth = OAuth1Session(self.client_key, client_secret=self.client_secret,
                                   signature_method=rfc5849.SIGNATURE_PLAINTEXT,
                                   callback_uri=HttpRequest.build_absolute_uri(request, reverse('access_token', kwargs={'pk': pk})))

        fetch_response = self.oauth.fetch_request_token(settings.HNP_OAUTH_URL + "/requestToken")

        self.resource_owner_key = fetch_response.get('oauth_token')
        self.resource_owner_secret = fetch_response.get('oauth_token_secret')
        request.session['resource_owner_key'] = self.resource_owner_key
        request.session['resource_owner_secret'] = self.resource_owner_secret

        url = "{base_url}/accessToken?oauth_consumer_key={consumer}&" + \
            "oauth_signature_method={sig_method}&" + \
            "oauth_signature={sig}&" + \
            "oauth_timestamp={timestamp}&" + \
            "oauth_nonce={nonce}&" + \
            "oauth_verifier={verifier}"
        url = url.format(base_url=settings.HNP_OAUTH_URL ,
                         consumer=hnp_oauth.client_name,
                         sig_method=rfc5849.SIGNATURE_PLAINTEXT,
                         sig=self.client_secret + "%26",
                         timestamp=int(time()),
                         nonce=int(time()*1.5),
                         verifier='ver')
        authorization_url = self.oauth.authorization_url(url=settings.HNP_OAUTH_URL  + "/authorization")

        return HttpResponseRedirect(redirect_to=authorization_url)


class AccessTokenView(View):

    def __init__(self):
        super().__init__()
        self.client_key = ''
        self.client_secret = ''
        self.oauth = ''

    def get(self, request, pk):
        hnp_oauth = HNPOAuth.objects.get(pk=self.kwargs['pk'])
        self.client_key = hnp_oauth.client_name
        self.client_secret = 'IMPLEMENT_SECRET'

        self.oauth = OAuth1Session(self.client_key, client_secret=self.client_secret,
                                   signature_method=rfc5849.SIGNATURE_PLAINTEXT,
                                   resource_owner_key=request.session.get('resource_owner_key', ''),
                                   resource_owner_secret=request.session.get('resource_owner_secret', ''))

        access_token_url = self.oauth.authorization_url(url=settings.HNP_OAUTH_URL + "/accessToken", request_token=request.GET['oauth_token'])
        redirect_response = reverse('access_token',
                                    kwargs={'pk': pk}) + "?oauth_token={0}&oauth_verifier={1}".\
            format(request.GET['oauth_token'], request.GET['oauth_verifier'])

        full_url = HttpRequest.build_absolute_uri(request, redirect_response)

        self.oauth.parse_authorization_response(full_url)
        access_token = self.oauth.fetch_access_token(access_token_url)

        hnp_oauth.token = access_token.get('oauth_token', '')
        hnp_oauth.save()

        return HttpResponseRedirect(redirect_to=request.session['referrer'])


class AddressGetView(View):

    def get(self,request,zipcode='',number='',hnp_token_id='',hnp_id=''):
        hnp_token_id = request.GET.get('token_id')
        hnp_id = request.GET.get('niki_id')
        zipcode = request.GET.get('zip')
        number = request.GET.get('nr')
        token = HNPOAuth.objects.get(pk=hnp_token_id).token
        cap = CreateApiRequest(token=token)
        try:
            response = cap.get("/direct/project/{0}/interest?zipcode={1}&number={2}".format(hnp_id, zipcode, number))
            return HttpResponse(json.dumps(
                {'success': {
                    'street': response.get('subscriber').get('street'),
                    'city': response.get('subscriber').get('city'),
                    'country': response.get('subscriber').get('country')
                }}), content_type="application/json")
        except ApiRequestException as are:
            return HttpResponse(
                {'error': are},
                content_type="application/json")
