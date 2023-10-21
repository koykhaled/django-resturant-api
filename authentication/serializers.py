from django.contrib.auth.models import User
from rest_framework import serializers

from django.contrib.auth import authenticate
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']


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
