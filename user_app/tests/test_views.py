import time

from unittest.mock import patch

from mozilla_django_oidc import views

from urllib.parse import parse_qs, urlparse

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import SuspiciousOperation
from django.test import RequestFactory, TestCase, Client, override_settings


User = get_user_model()

def my_custom_op_logout(request):
    return request.build_absolute_uri('/logged/out')

class OIDCAuthorizationCallbackViewTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    @override_settings(LOGIN_REDIRECT_URL='/success')
    def test_get_auth_success(self):
        user = User.objects.create_user('username')
        get_data = {
            'code' : 'example_code',
            'state' : 'example_state'
        }
        url = reverse('oidc_authentication_callback')
        request = self.factory.get(url, get_data)
        client = Client()
        request.session = client.session
        request.session['oidc_states'] = {
            'example_state' : {'nonce': None, 'added_on': time.time()}
        }
        callback_view = views.OIDCAuthenticationCallbackView.as_view()

        with patch('mozilla_django_oidc.views.auth.authenticate') as mock_auth:
            with patch('mozilla_django_oidc.views.auth.login') as mock_login:
                mock_auth.return_value = user
                response = callback_view(request)

                mock_auth.assert_called_once_with(nonce=None, request=request)
                mock_login.assert_called_once_with(request, user)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/success')