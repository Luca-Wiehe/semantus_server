"""
Django models define the format of data in the database. We have a database for user data, 
a database for contact data, and a database for words.
"""
from django.db import models


class UserData(models.Model):
    """
    Table of users
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
    Table of contacts
    """

    # create an entry based on foreign key (username)
    # models.CASCADE ensures that if one of the users is deleted, the contact is deleted as well
    user1 = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name="+")
    user2 = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name="+")

    # does user1 have user2 as a favorite
    favorite1 = models.BooleanField(default=False)

    # does user2 have user1 as a favorite
    favorite2 = models.BooleanField(default=False)

    # is contact request still pending
    pending = models.BooleanField(default=True)


class WordData(models.Model):
    """
    Table of Words
    """

    word_id = models.CharField(max_length=20, unique=True, null=True)
    word = models.CharField(max_length=20, unique=True, null=True)


class Game(models.Model):
    """
    Table of games
    """

    game_id = models.CharField(max_length=20, unique=True, null=True)
    game_type = models.CharField(max_length=20, default="coop")
    creator_id = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name="+")
    start_time = models.DateTimeField(auto_now_add=True)
    word_id = models.ForeignKey(WordData, on_delete=models.CASCADE, related_name="+")


class GameParticipants(models.Model):
    """
    Table of game participants
    """

    game_id = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="+")
    user_id = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name="+")
    best_guess = models.DecimalField(max_digits=10, decimal_places=2)


class GameGuesses(models.Model):
    """
    Table of guesses in a game
    """

    game_id = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="+")
    user_id = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name="+")
    guess = models.CharField(max_length=20, unique=True, null=True)
    similarity = models.DecimalField(max_digits=10, decimal_places=2)


class GameInvitations(models.Model):
    """
    Table of game invitations
    """

    game_id = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="+")
    user_id = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name="+")
    accepted = models.BooleanField(default=False)
