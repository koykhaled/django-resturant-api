from django.db import models
from django.contrib.auth.models import User , Group


# Create your models here.

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=50,unique=True)
    
    def __str__(self):
        return self.title
    
    
    
class MenuItems(models.Model):
    title = models.CharField(max_length=100,unique=True)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    featured = models.BooleanField()
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    
    def __str__(self):
        return self.title
    

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItems,on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    
    class Meta:
        unique_together = ('user','menu_item')


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User,on_delete=models.CASCADE,related_name="delivery_crew")
    quantity = models.SmallIntegerField()
    status = models.BooleanField(db_index=True,default=0)
    total = models.DecimalField(max_digits=6,decimal_places=2)
    
    def __str__(self):
        return str(self.user)+ " ord"+str(self.id)


class OrderItems(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItems,on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    total = models.DecimalField(max_digits=6,decimal_places=2)
    
    class Meta:
        unique_together = ('order','menu_item')
    def __str__(self):
        return str(self.menu_item)


class GroupMembership(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.user.username) + "_" + str(self.group.name)
