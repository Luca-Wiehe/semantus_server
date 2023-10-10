"""
Views are responsible for handling requests and returning responses.
This requires the use of serializers to obtain data from models (i.e.
data tables) and convert them to JSON format.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.db import IntegrityError
from django.utils.text import slugify

import firebase_admin.auth as auth

from .serializers import UserDataSerializer
from .models import UserData, GameParticipants, GameGuesses, WordData

import re
import spacy
import random
import string

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


class JoinGameView(APIView):
    """
    Goal: Create or join a game

    Requests:
        - POST: Create a new game
        - GET: Join an existing game
    """

    def get(self, request, *args, **kwargs):
        """
        GET-request to join a game

        Request Headers:
            - Authorization: Firebase Token for authentication

        Request Parameters:
            - game_id: id of the game to join
        """
        # derive player_id from token (else return unauthorized)
        token = request.headers.get("Authorization")

        # get game_id

        # check if game_id exists (if not, specify in error that the game has ended)

        # check if player is invited to game
        # invited = is_invited(game_id, player_id)
        invited = False

        if invited:
            # check if user accepts or declines invitation
            invitation_accepted = False

            if invitation_accepted:
                # add user to GameParticipants table

                # remove invitation from GameInvitations table

                # serialize GameData of the game_id

                # return successful response with game_data
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                # remove invitation from GameInvitations table
                return Response(status=status.HTTP_202_ACCEPTED)

        else:
            # throw unauthorized error
            pass

    def post(self, request, *args, **kwargs):
        """
        POST-request to create a game

        Request Headers:
            - Authorization: Firebase Token for authentication

        Request Parameters:
            - game_type: type of game to create (singleplayer, coop, versus)
        """
        # derive player_id from token (else return unauthorized)

        # get game_type

        # return 501 error if game_type is not singleplayer, coop or versus

        # check if user is already part of a game with the same game_type

        # if yes, return 409 error

        # else create game

        # add user to GameParticipants table

        # serialize game_id

        # generate random game_id with 20 characters
        game_id = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(20)
        )

        # return game_id
        pass


class InviteView(APIView):
    """
    Goal: Invite friends to game

    POST request for inviting a new person
    """

    def post(self, request, *args, **kwargs):
        """
        POST request to invite friend to a game
        """
        pass

    pass


class GameView(APIView):
    """
    Goal: Get and modify game data

    GET request for getting game state

    POST request for modifying game state (i.e. adding a new word)
    """

    def get(self, request, *args, **kwargs):
        game_id = request.query_params.get("game_id", None)

        # obtain user from token
        firebase_data = verify_firebase_token(request)

        # return error if firebase authentication fails
        if isinstance(firebase_data, Response):
            return firebase_data

        user_id, user = firebase_data

        # check if user is part of current game based on GameParticipants table
        try:
            GameParticipants.objects.get(game_id=game_id, user_id=user.username)

            # if yes, serialize game data and return it

        # else return unauthorized error
        except GameParticipants.DoesNotExist:
            return Response(
                {"detail": "User is not part of this game."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def post(self, request, *args, **kwargs):
        game_id = request.query_params.get("game_id", None)

        # obtain game_id and word from request
        word = request.query_params.get("word", None)

        # obtain user from token
        firebase_data = verify_firebase_token(request)

        # return error if firebase authentication fails
        if isinstance(firebase_data, Response):
            return firebase_data

        # otherwise, we get user_id and user
        _, user = firebase_data

        try:
            # make sure that user is part of current game based on GameParticipants table
            GameParticipants.objects.get(game_id=game_id, user_id=user.username)

            # lemmatize word
            language_model = spacy.load("de_core_news_sm")
            doc = language_model(word)

            if len(doc) == 0:
                return Response(
                    {"detail": "Unknown word provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            lemmatized_word = doc[0].lemma_

            # check if lemmatized_word is in WordData table
            WordData.objects.get(word=lemmatized_word)

            # get word embeddings for lemmatized_word and target_word

            # compute similarity to target word
            similarity = 0

            # add word to GameGuesses table
            guess = GameGuesses(
                game_id=game_id,
                user_id=user.username,
                guess=lemmatized_word,
                similarity=similarity,
            )

            try:
                # try to save new entry
                guess.save()

                # serialize GameData

                # return GameData as part of response

            # integrity error if word has already been guessed
            except:
                # serialize GameData

                # return GameData as part of response

                return Response(
                    {"detail": "Word has already been guessed."},
                    status=status.HTTP_409_CONFLICT,
                )

        # user not found => unauthorized
        except GameParticipants.DoesNotExist:
            return Response(
                {"detail": "User is not part of this game."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


def verify_firebase_token(request):
    """
    Verifies the firebase token passed in the request header.

    Returns:
        - uid: Firebase user id
        - user: UserData object
        - Response object if an error occurs
    """
    # obtain user_id from token
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
            return uid, user

        except UserData.DoesNotExist:
            return Response(
                {"detail": "User does not exist. Please sign up."},
                status=status.HTTP_404_NOT_FOUND,
            )

    # if firebase authentication fails, we get an exception and return a 401 error to the user
    except Exception:
        return Response(
            {"detail": "Invalid firebase token provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
