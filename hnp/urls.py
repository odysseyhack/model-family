from django.conf.urls import url
from .views import RequestTokenView, AccessTokenView, AddressGetView


urlpatterns = [
    url(r'^request_token/(?P<pk>[0-9]+)$', RequestTokenView.as_view(), name='request_token'),
    url(r'^access_token/(?P<pk>[0-9]+)/$',
        AccessTokenView.as_view(), name='access_token'),
    url(r'^request_address/$', AddressGetView.as_view(), name='request_address')
]
