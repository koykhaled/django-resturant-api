from rest_framework import serializers
from .models import *


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMembership
        fields = ['user','group']
        
    # def validate(self, validated_data):
    #     user = validated_data['user']
    #     group = validated_data['group']
    #     if user and group :
    #         user_group = GroupMembership.objects.create(
    #             user = user,
    #             group=group
    #         )
    #         user_group.save()
    #         return user_group
    #     raise serializers.ValidationError({"error" : "user or group not found"})
