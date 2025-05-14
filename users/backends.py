from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Authentication backend which allows users to log in using either username or email
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        # Try to find the user by either username or email
        try:
            # Use Q objects to create an OR query
            user = UserModel.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=username)
            ).first()

            # Check password if user exists
            if user and user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            # Return None if the user doesn't exist
            return None

        return None
