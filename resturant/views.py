from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status 
from .permissoins import IsManager
from .serializers import GroupMemberSerializer
from .models import GroupMembership
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User , Group


# Create your views here.


class GroupMemeberView(APIView):
    permission_classes = [IsAuthenticated,IsManager]
    serializer_class = GroupMemberSerializer
    # get users that assigne to groups
    def get(self,request):
        
        user_group = GroupMembership.objects.all()
        serializer = self.serializer_class(user_group,many=True)
        if len(serializer.data)  :
            return Response({"data":serializer.data},status=status.HTTP_200_OK)
        return Response({"message" : "no Users in Groups"},status=status.HTTP_404_NOT_FOUND)
    
    
    # assign users to groups
    def post(self,request,user_id):
        user = get_object_or_404(User,id=user_id)
        group_id = request.data.get('group')
        group = get_object_or_404(Group,id=group_id)
        
        if GroupMembership.objects.filter(user=user,group=group).exists() :
            return Response({"message" : "User already in this group"},status=status.HTTP_400_BAD_REQUEST)
        user_group = GroupMembership.objects.create(user=user,group=group)
        user_group.save()
        return Response({"message" : "adding user to group done"},status=status.HTTP_200_OK)
    
    
    def put(self, request, user_id,group_id):
        user = get_object_or_404(User, id=user_id)
        group = get_object_or_404(Group, id=group_id)
        user_group = get_object_or_404(GroupMembership,user=user,group=group)
        new_group = get_object_or_404(Group, id=request.data.get('group'))

        user_group.group = new_group
        user_group.save()

        serializer = GroupMemberSerializer(user_group)
        return Response({"data":serializer.data,"message":"update User Group Done"},status=status.HTTP_200_OK)

        
    def patch(self, request, user_id,group_id):
        try :
            user = get_object_or_404(User, id=user_id)
            group = get_object_or_404(Group, id=group_id)
            user_group = get_object_or_404(GroupMembership,user=user,group=group)
            new_group = get_object_or_404(Group, id=request.data.get('group'))

            user_group.group = new_group
            user_group.save()

            serializer = GroupMemberSerializer(user_group)
            return Response({"data":serializer.data,"message":"update User Group Done"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)

            
    
    # delete users from groups
    def delete(self,request,user_id,group_id):
        try:
            user = GroupMembership.objects.filter(user=user_id,group=group_id)
            if  user.exists() :
                user.delete()
                return Response({"message":"Delete user from group Done"},status=status.HTTP_200_OK)

            return Response({"message":"Not Found"},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"message" : "User Not Found"},status=status.HTTP_404_NOT_FOUND)