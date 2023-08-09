"""
Serializers are used to convert information obtained from Django database (stored in models) to JSON format.
"""

from rest_framework import serializers

from .settings import all_fields
from .models import UserData


class UserDataSerializer(serializers.ModelSerializer):
    """
    Serializes all information from the PersonalData model that is safe for users to see
    """

    class Meta:
        model = UserData
        fields = [x for x in all_fields if x != "firebase_id"]
