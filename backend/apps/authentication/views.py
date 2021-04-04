from rest_framework.response import Response
from django.shortcuts import render
from .models import User
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserAuthSerializer, PasswordSerializer,BulkCreateUserSerializer, UsersSerializer

class LoginViews(APIView):

    def message(self,message,status,data):
        response = {
                "message":message, 
                "status":status,
                "data" : data
            }
        return response

    def get_user_data(self, email, password):
        try:
            obj = User.objects.get(email=email)
            if obj.is_active == True:
                return obj
            else:
                return 'Inactive'
        except User.DoesNotExist: 
            return ''

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

    def post(self, request):
        data = request.data
        user = self.get_user_data(email=data['email'],password= data['password'])
        if user != '' and user != 'Inactive':
            message = "Login successful"
            status_server = status.HTTP_200_OK
            serializer = UserAuthSerializer(user)
            data = {
                "tokens": self.get_tokens_for_user(user=user),
                "user" : serializer.data,
                }
        elif user == 'Inactive':
            message = "This user is disable"
            status_server = status.HTTP_401_UNAUTHORIZED
            data = {}
        else:
            message = "Email and password are wrong"
            status_server = status.HTTP_401_UNAUTHORIZED
            data = {}
        res = self.message(message, status_server, data)
        return Response(res, status = status_server)



class CreateUsersView(APIView):

    permission_classes =  [IsAuthenticated]

    def message(self,message,status,data):
        response = {
                "message":message, 
                "status":status,
                "data" : data
        }
        return response

    def post(self,request):
        data = request.data
            
        serializer = BulkCreateUserSerializer(data=data)
        if not serializer.is_valid():
            message = "Wrond data"
            status_server = status.HTTP_400_BAD_REQUEST
            data = serializer.errors
            res = self.message(message, status_server, data)
            return Response(res, status = status_server)

        password = data['first_name'] + data['last_name']
        user = User.objects.create(**data, password=password)
        message = "Usuarios creados correctamente"
        status_server = status.HTTP_201_CREATED
        serializer = UsersSerializer(user)
        data = serializer.data
        res = self.message(message, status_server, data)
        return Response(res, status = status_server)
