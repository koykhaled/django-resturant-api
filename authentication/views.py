from django.shortcuts import render
from .serializers import RegisterSerializer , LoginSerializer
from rest_framework.decorators import APIView , api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

# Create your views here.


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        access_token = AccessToken.for_user(user)
        payload = {
            "user" : {
                "username" : user.username,
                "email" : user.email
            },
            "token" : str(access_token)
        }
        return Response(payload,status=status.HTTP_201_CREATED)


class LoginView(APIView):
    serializer_class = LoginSerializer
    
    # def post(self,request):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.save()
    #     access_token = AccessToken.for_user(user)
    #     payload = {
    #         "user" : {
    #             "username" : user.username,
    #             "email" : user.email
    #         },
    #         "token" : str(access_token)
    #     }
    #     return Response(request.data,status=status.HTTP_200_OK)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        refresh = AccessToken.for_user(user)

        return Response({
            'access': str(refresh),
            }, status=status.HTTP_200_OK)
    


# @api_view()
# @permission_classes([IsAuthenticated])
# def secret(request):
#     return Response({"message" : "Mesaage"})