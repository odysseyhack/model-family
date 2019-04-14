"""hackathon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import oauth2_provider.views as oauth2_views
from django.conf import settings
from django.views.generic import TemplateView
from hackathon.views import ApiEndpointCreateBuilding, LogInView, ResendActivationCodeView, RemindUsernameView, SignUpView, ActivateView, LogOutView, ChangeEmailView, ChangeEmailActivateView, ChangeProfileView, ChangePasswordView, RestorePasswordView, RestorePasswordDoneView, RestorePasswordConfirmView, BuildingCreateView
# OAuth2 provider endpoints
oauth2_endpoint_views = [
	path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
	path('token/', oauth2_views.TokenView.as_view(), name="token"),
	path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
	# OAuth2 Application Management endpoints
	oauth2_endpoint_views += [
		 path('applications/', oauth2_views.ApplicationList.as_view(), name="list"),
		 path('applications/register/', oauth2_views.ApplicationRegistration.as_view(), name="register"),
		 path('applications/<int:pk>/', oauth2_views.ApplicationDetail.as_view(), name="detail"),
		 path('applications/<int:pk>/delete/', oauth2_views.ApplicationDelete.as_view(), name="delete"),
		path('applications/<int:pk>/update/', oauth2_views.ApplicationUpdate.as_view(), name="update"),
	]

	# OAuth2 Token Management endpoints
	oauth2_endpoint_views += [
	   path('authorized-tokens/$', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
	   path('authorized-tokens/(?P<pk>\d+)/delete/$', oauth2_views.AuthorizedTokenDeleteView.as_view(),
			name="authorized-token-delete"),
	]

urlpatterns = [
	path('api-auth/', include('rest_framework.urls')),
	path('admin/', admin.site.urls),
	path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
	path('api/building', ApiEndpointCreateBuilding.as_view()),

	path('create/building', BuildingCreateView.as_view(success_url="/success/"), name='create_building'),
	
	
	path('log-in/', LogInView.as_view(), name='log_in'),
	path('log-out/', LogOutView.as_view(), name='log_out'),

	path('resend/activation-code/', ResendActivationCodeView.as_view(), name='resend_activation_code'),

	path('sign-up/', SignUpView.as_view(), name='sign_up'),
	path('activate/<code>/', ActivateView.as_view(), name='activate'),

	path('restore/password/', RestorePasswordView.as_view(), name='restore_password'),
	path('restore/password/done/', RestorePasswordDoneView.as_view(), name='restore_password_done'),
	path('restore/<uidb64>/<token>/', RestorePasswordConfirmView.as_view(), name='restore_password_confirm'),

	path('remind/username/', RemindUsernameView.as_view(), name='remind_username'),

	path('change/profile/', ChangeProfileView.as_view(), name='change_profile'),
	path('change/password/', ChangePasswordView.as_view(), name='change_password'),
	path('change/email/', ChangeEmailView.as_view(), name='change_email'),
	path('change/email/<code>/', ChangeEmailActivateView.as_view(), name='change_email_activation'),

	path('success/', TemplateView.as_view(template_name="success.html"), name='success'),
	path('', TemplateView.as_view(template_name="home.html"), name='home'),

]
