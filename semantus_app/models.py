"""
Django models define the format of data in the database. We have a database for user data, 
a database for contact data, and a database for words.
"""
from django.db import models
from django.contrib.postgres.fields import ArrayField

class UserData(models.Model):
    """
    Database of users
    """

    # fields that are required for a user
    firebase_id = models.CharField(max_length=100, unique=True, null=True)
    username = models.CharField(max_length=20, unique=True, null=True)

    # personal data
    avatar = models.CharField(max_length=20, default="default")
    points = models.IntegerField(default=2000)

    # game logic attributes
    current_singleplayer_word = models.CharField(max_length=20, default="word_id")
    current_multiplayer_game_id = models.CharField(max_length=20, default="game_id")

    REQUIRED_FIELDS = ["firebase_id", "username"]


class Contact(models.Model):
    """
    Database of contacts
    """

    # create an entry based on foreign key (username)
    # models.CASCADE ensures that if one of the users is deleted, the contact is deleted as well
    user1 = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name="+")
    user2 = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name="+")
