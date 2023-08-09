"""
Views are responsible for handling requests and returning responses.
This requires the use of serializers to convert data to JSON format.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.db import IntegrityError
from django.utils.text import slugify

import firebase_admin.auth as auth

from .serializers import UserDataSerializer
from .models import UserData

import re

"""
TODO: What requests do we need to support?

Login Requests:
    - POST login (firebase_token)
    - GET logout(firebase_token) 

Personal Data Requests:
    - POST update_user(firebase_token, avatar, privacy_settings)
    - POST delete_user(firebase_token)

Game Requests:
    - GET get_daily()
    - POST new_multiplayer_game()
    - POST join_multiplayer_game()

Friend Requests:
    - POST add_friend(firebase_token, username)
    - POST remove_friend(firebase_token, username)
    - GET friend_list(firebase_token)
"""


class HomepageView(APIView):
    """
    Goal: Check whether the website is available.
    Authentication: Not required.
    """

    authentication_classes = []
    permission_classes = []

    def get(self, _):
        return Response(status=status.HTTP_200_OK)


class UsernameCheckView(APIView):
    """
    Goal: Check whether a username is available.
    Authentication: Not required.
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        username = request.query_params.get("username", None)

        if not username:
            return Response(
                {"message": "In der Request ist kein 'username' Parameter enthalten."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate username format
        if not re.match(r"^[a-zA-Z0-9_äöüÄÖÜß]+$", username):
            return Response(
                {
                    "message": "Usernames dürfen nur Buchstaben, Zahlen und Unterstriche enthalten."
                },
                status=status.HTTP_200_OK,
            )

        if UserData.objects.filter(username__iexact=username).exists():
            return Response(
                {"message": "Username ist vergeben"}, status=status.HTTP_200_OK
            )

        else:
            return Response(
                {"message": "Username ist verfügbar"}, status=status.HTTP_200_OK
            )


class LoginView(APIView):
    """
    Goal: Authenticate users using their firebase token.
    """

    permission_classes = [
        AllowAny,
    ]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")

        # if no token is passed, we return a 401 error right away
        if not token:
            print("\nNo token provided!\n")
            return Response(
                {"detail": "Invalid input. Please provide a firebase token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # otherwise, we try to verify the token using firebase
        try:
            decoded_token = auth.verify_id_token(token)

            uid = decoded_token["uid"]

            try:
                user = UserData.objects.get(firebase_id=uid)

            except UserData.DoesNotExist:
                return Response(
                    {"detail": "User does not exist. Please sign up."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = UserDataSerializer(user)

            return Response(serializer.data, status=status.HTTP_200_OK)

        # if firebase authentication fails, we get an exception and return a 401 error to the user
        except Exception:
            return Response(
                {"detail": "Invalid firebase token provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class SignupView(APIView):
    """
    Goal: Add new users to the database and validate their firebase token.
    """

    permission_classes = [
        AllowAny,
    ]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")
        username = request.query_params.get("username")

        # if no token is passed, we return a 401 error right away
        if not token:
            print("\nNo token provided!\n")
            return Response(
                {"detail": "Invalid input. Please provide a firebase token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # otherwise, we try to verify the token using firebase
        try:
            decoded_token = auth.verify_id_token(token)

            uid = decoded_token["uid"]

            try:
                print(f"Creating user with username: {username}")
                user = UserData.objects.create(firebase_id=uid, username=username)

            except IntegrityError:
                return Response(
                    {"detail": "User does already exist. Please log in."},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

            except Exception as e:
                print(e)
                return Response(
                    {"detail": "Internal server error."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            serializer = UserDataSerializer(user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # if firebase authentication fails, we get an exception and return a 401 error to the user
        except Exception as e:
            print(e)

            return Response(
                {"detail": "Invalid firebase token provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
