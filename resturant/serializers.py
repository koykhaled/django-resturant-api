from rest_framework import serializers
from .models import *


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMembership
        fields = ['user','group']
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'slug']



class MenuItemsSerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source="category")
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItems
        fields = ['title','price','featured','category_id','category_name']
        
    def get_category_name(self, obj):
        return obj.category.title
    
    def update(self, instance, validated_data):
        for field in validated_data:
            setattr(instance, field, validated_data[field])
        instance.save()
        return instance