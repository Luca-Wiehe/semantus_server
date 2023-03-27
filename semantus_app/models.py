from django.db import models
from django.contrib.auth.models import AbstractUser

class UserData(AbstractUser):
    """
    User data necessary for identification/authentication.
    AbstractUser:
        required: username, password
        optional: email, first_name, last_name
    """
    points = models.IntegerField(default=2000)
