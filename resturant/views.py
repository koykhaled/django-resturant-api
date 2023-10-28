from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import APIView , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status , filters
from .permissoins import IsManager , IsDeliveryCrew
from .serializers import GroupMemberSerializer , MenuItemsSerializer , CartSerializer , OrderSerializer
from .models import GroupMembership
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User , Group
from .models import MenuItems , Category , Cart , Order, OrderItems
import decimal



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





class MenuItemsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuItemsSerializer
    filter_backends = [filters.SearchFilter]

    def get(self,reuqest):
        search = reuqest.query_params.get('search',)
        price = reuqest.query_params.get('price',)
        category = reuqest.query_params.get('category')
        menu_items = MenuItems.objects.all()
        if search :
            menu_items = MenuItems.objects.filter(title__icontains=search)
        if category :
            category_id = Category.objects.filter(title__icontains=category).get().id
            menu_items = MenuItems.objects.filter(category=category_id)
        if price :
            menu_items = MenuItems.objects.filter(price__lte=price)
        serializer = self.serializer_class(menu_items,many=True)
        if len(serializer.data) > 0:
            return Response({"data" : serializer.data}, status=status.HTTP_200_OK)
        return Response ({"message":"no items in menu"})


    def post(self,request):
        if not IsManager().has_permission(request,self) :
            return Response({"message" : "permission denied"},status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data" : serializer.data,"message" : "adding new item done".capitalize()},status=status.HTTP_201_CREATED)


    def put(self,request,item_id):
        try:
            if not IsManager().has_permission(request,self) :
                return Response({"message" : "permission denied"},status=status.HTTP_403_FORBIDDEN)

            menu_item = get_object_or_404(MenuItems,id=item_id)
            menu_item.title = request.data.get('title') or menu_item.title
            menu_item.price = request.data.get('price') or menu_item.price
            menu_item.featured = request.data.get('featured') or menu_item.featured
            menu_item.save()
            serializer = self.serializer_class(menu_item)
            return Response({"data" : serializer.data ,"message":"updating item done"},status=status.HTTP_200_OK)
        except Exception as e :
                return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self,request,item_id):
        try:
            if not IsManager().has_permission(request,self) :
                return Response({"message" : "permission denied"},status=status.HTTP_403_FORBIDDEN)

            menu_item = get_object_or_404(MenuItems,id=item_id)
            menu_item.title = request.data.get('title') or menu_item.title
            menu_item.price = request.data.get('price') or menu_item.price
            menu_item.featured = request.data.get('featured') or menu_item.featured
            menu_item.save()
            serializer = self.serializer_class(menu_item)
            return Response({"data" : serializer.data ,"message":"updating item done"},status=status.HTTP_200_OK)
        except Exception as e :
                return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self,request,item_id):
        try:
            if not IsManager().has_permission(request,self) :
                return Response({"message" : "permission denied"},status=status.HTTP_403_FORBIDDEN)

            menu_item = get_object_or_404(MenuItems,id=item_id)
            if menu_item :
                menu_item.delete()
                return Response({"message":"Item deleted done"},status=status.HTTP_200_OK)
        except Exception as e: 
            return Response({"error" : "Item not found in menu"})



class CartView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    
    def get(self,request):
        user = User.objects.get(id=request.user.id)
        cart_items = Cart.objects.filter(user=user)
        serializer = self.serializer_class(cart_items,many=True)
        if len(serializer.data)>0:
            return Response({"data" : serializer.data})
        return Response ({"message":"no items in menu"})
    
    def post(self,request):
        user = User.objects.get(id=request.user.id)
        item_id = request.data.get('item_id')
        menu_item = get_object_or_404(MenuItems,id=item_id)
        quantity = request.data.get('quantity')
        unit_price = menu_item.price
        price = decimal.Decimal(quantity) * unit_price
        cart = Cart.objects.create(
            user = user,
            menu_item=menu_item,
            quantity=quantity,
            unit_price=unit_price,
            price=price
        )
        cart.save()
        serializer = self.serializer_class(cart)
        print(menu_item)
        return Response({"me" : serializer.data})


class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    
    def post(self,request):
        user = User.objects.get(id=request.user.id)

        group = Group.objects.get(name='delivery_crew')
        delivery_crew = get_object_or_404(GroupMembership,user=request.data.get('delivery_id'),group=group)
        delivery = get_object_or_404(User,id=delivery_crew.user.id)
        

        cart_items = Cart.objects.filter(user=user)
        if len(cart_items) == 0 :
            return Response({"message" : "No items i cart"})
        

        status = request.data.get('status')
        quantity = 0
        totla_price = 0
        for cart in cart_items:
            quantity += cart.quantity
            totla_price += cart.price
        
        order = Order.objects.create(
            user=user,
            delivery_crew=delivery,
            quantity=quantity,
            total=totla_price,
            status=status
        )
        for order_item in cart_items :
            OrderItems.objects.create(
                order=order,
                menu_item=order_item.menu_item,
                quantity=cart.quantity,
                unit_price=cart.unit_price,
                total=cart.price
            )
        serializer = self.serializer_class(order)
        return Response({"data" : serializer.data})
    
    def put(self,request,order_id):
        if not IsDeliveryCrew().has_permission(request,self):
            return Response({"message" : "Permission Denied"})
        order = Order.objects.get(id=order_id)
        order.status = request.data.get('status')
        order.save()
        if order.status == "True":
            return Response({"message" : f"{order} Order Deliverd Successfully"})
        return Response({"message" : f"{order} Not Deliverd Yet"})
        