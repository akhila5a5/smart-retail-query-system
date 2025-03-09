from django.db import models
import os
# Create your models here.


class UserModel(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = "UserModel"



# models.py

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)  
    image = models.ImageField(upload_to=os.path.join('static', 'ProductImages'), null=True)
    color=models.CharField(max_length=100,default="Unknown")
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "Product"


class Cart(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = "Cart"


class Orders(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cardholdername = models.CharField(max_length=100)
    cardnumber = models.IntegerField()
    expirationdate = models.CharField(max_length=100)
    cvv = models.IntegerField()
    quantity = models.IntegerField(null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='Order Placed')

    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = "Orders"