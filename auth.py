from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from user_app.models import User

class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):

    """CustomOIDCAuthenticationBackend"""

    def get_email(self, claims):
        email = claims.get('email')
        if not email:
            email = claims.get('sub')
        return email

    def filter_users_by_claims(self, claims):
        """Create user with email base custom user model."""
        email = self.get_email(claims)
        if not email:
            return self.UserModel.objects.none()
        try:
            return self.UserModel.objects.filter(email=email)
        except self.UserModel.DoesNotExist:
            return self.UserModel.objects.none()

    def create_user(self, claims):
        """Create user with email base custom user model."""
        # email = self.get_email(claims)
        # return self.UserModel.objects.create_user(email)
        user = super(CustomOIDCAuthenticationBackend, self).create_user(claims)
        user.email = self.get_email(claims)
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.phone_number = claims.get('phone_number', '')
        user.save()

        return user

    def update_user(self, user, claims):
        user.first_name = claims.get('given_name')
        user.last_name = claims.get('family_name')
        user.phone_number = claims.get('phone_number', '')
        user.save()

        return user