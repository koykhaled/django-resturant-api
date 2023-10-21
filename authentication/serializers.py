from django.contrib.auth.models import User
from rest_framework import serializers

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username','email' ,'password']

    def create(self, validated_data):
        user = User(
        username=validated_data['username'],
        email=validated_data['email']
        )
        password = validated_data['password']
        user.password = make_password(password) 
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        username = data.get('username','')
        password = data.get('password','')
        
        user = authenticate(username=username,password=password)
        if user and user.is_active:
            return {"user" : user}
        raise serializers.ValidationError({"error":"invalid credentials"})
