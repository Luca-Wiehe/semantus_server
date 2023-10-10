"""
This file defines authentication methods that will be used by the API. In
particular, we use Firebase authentication tokens to verify the identity
of users. Users will have to obtain their firebase token on the client side
and send it as a header with each request.
"""

from django.contrib.auth.models import User
from rest_framework import authentication
import firebase_admin.auth as auth


class FirebaseAuthentication(authentication.BaseAuthentication):
    """
    Authentication class for Firebase Users
    """

    def authenticate(self, request):
        """
        Authenticates users with firebase tokens

        Returns:
            user: User object if authentication was successful. None otherwise.
        """

        # extract token from header
        token = request.header.get("Authorization")

        # if no token is provided, return None
        if not token:
            return None

        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token["uid"]

        # if the token is invalid, verify_id_token will throw an exception
        except:
            return None

        # if the token is valid, check if the user already exists in the database (if not, create a new user)
        try:
            user = User.objects.get(firebase_id=uid)
            return user

        except:
            return None
