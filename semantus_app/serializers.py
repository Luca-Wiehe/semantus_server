"""
Serializers are used to convert information obtained from Django database (stored in models) to JSON format.
"""

from rest_framework import serializers

from .settings import all_fields
from .models import UserData, Game


class UserDataSerializer(serializers.ModelSerializer):
    """
    Serializes all information from the PersonalData model that is safe for users to see
    """

    class Meta:
        model = UserData
        fields = [x for x in all_fields if x != "firebase_id"]


class GameDataSerializer(serializers.ModelSerializer):
    """
    Serializes all information from the GameData model that is safe for users to see
    """

    class Meta:
        # return all data from GameData (i.e. start_time, owner, etc.)
        model = Game
        fields = []

        # additionally, return data from GameGuesses (i.e. guess, guesser, etc.)
