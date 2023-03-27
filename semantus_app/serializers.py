from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .settings import id_fields
from .models import UserData

class UserSerializer(serializers.ModelSerializer):
    """
    Serializes all information from the PersonalData model that is safe for users to see
    """
    class Meta:
        model = UserData
        fields = [x for x in id_fields if x != 'password']


class SignupSerializer(serializers.ModelSerializer):
   """
   Goal: Validate user information during signup. Avoid duplicates of usernames and emails. 
   Assumption: Passwords are validated in the frontend.
   """
   class Meta:
      model = UserData
      fields = id_fields
      extra_kwargs = {
         'username': {
            'validators': [ UniqueValidator(queryset=UserData.objects.all()) ], # username unique
            'required': True
         },
         'email': {
            'validators': [ UniqueValidator(queryset=UserData.objects.all()) ], # email unique
            'required': True
         }, 
         'password': {
            'write_only': True, # don't send password back to user
            'required': True
         }
      }

   def create(self, validated_data):
      """
      Goal: Encrypt password in the database to match password from ObtainAuthToken.  
      """
      password = validated_data.pop('password')
      user = UserData(**validated_data)
      user.set_password(password)
      user.save()
      
      return user
