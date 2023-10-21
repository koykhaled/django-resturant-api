from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status 
from .permissoins import IsManager

# Create your views here.


class Manager(APIView):
    permission_classes = [IsAuthenticated,IsManager]
    def check(self,request):
        return Response({"message":"Done"})