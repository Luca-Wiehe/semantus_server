from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import SignupSerializer

class HomepageView(APIView):
   """
   Goal: Check whether the website is available. 
   Authentication: Not required.
   """
   authentication_classes = []
   permission_classes = []

   def get(self, _):
      return Response(status=status.HTTP_200_OK)

class SignupView(ObtainAuthToken):
   """
   Goal: Add new users to the database and provide them with a token. 
   """
   def post(self, request, *args, **kwargs):
      serializer = SignupSerializer(data=request.data)

      if serializer.is_valid():
         user = serializer.save()

         if user:
            token = Token.objects.create(user=user)
            json = serializer.data
            json['token'] = token.key

            return Response(json, status=status.HTTP_201_CREATED)

      if "username" in serializer.errors.keys():
         return Response({"detail": "Invalid input. Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
      
      if "email" in serializer.errors.keys():
         return Response({"detail": "Invalid input. Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

      return Response(status=status.HTTP_400_BAD_REQUEST)

class LoginView(ObtainAuthToken):
   """
   Goal: Obtain token for users who give correct credentials.
   """
   