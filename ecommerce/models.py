from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="customer")
    name=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    
    def __str__(self):
        return str(self.user)
 
CATEGORY=(
    ('smartphones','Smart-phones'),
    ('tablets','Tablets'),
    ('television','Television'),
    ('smartwatches','Smart-watches')
    )
LABEL=(
    ('new','New'),
    ('best-seller','Best-seller')
    )   
class Product(models.Model):
    name=models.CharField(max_length=120)
    image=models.ImageField(upload_to="images/",default=False)
    price=models.FloatField()
    discount_price=models.FloatField(blank=True,null=True)
    category=models.CharField(choices=CATEGORY,max_length=40)
    label=models.CharField(choices=LABEL,max_length=40)
    launched_date=models.DateTimeField(auto_now_add=True)
    date=models.DateTimeField(auto_now_add=True)
    description=models.TextField()

    def __str__(self):
        return self.name
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,blank=True,null=True,related_name="customer_order")
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)
    transacition_id=models.CharField(max_length=120,null=True)
    
    
    def __str__(self):
        return str(self.id)
    
    
    @property
    def get_total(self):
        #reverse relation from OrderItem
        orderitems=self.order.all()
        total=sum(i.final_price() for i in orderitems)
        return total
    @property
    def get_total_item(self):
        #reverse relation from OrderItem
        orderitems=self.order.all()
        total=sum(i.quantity for i in orderitems)
        return total
    
class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="order_item")
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order")
    quantity=models.IntegerField(default=0,blank=True,null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def discount(self):
        return self.product.discount_price*self.quantity
    def price(self):
        return self.product.price*self.quantity
    
    def final_price(self):
        if self.product.discount_price:
            return self.price()-self.discount()
        else:
            return self.price()
    
    
        
class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE,related_name="customer_shipping")
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_shipping")
    address=models.CharField(max_length=255,null=True)
    city=models.CharField(max_length=255,null=True)
    country=models.CharField(max_length=255,null=True)
    zipcode=models.CharField(max_length=255,null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.address)
    
class Contact(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField(max_length=200)
    phone=models.CharField(max_length=200)
    description=models.TextField()
    
    def __str__(self):
        return str(self.first_name)

    
    
    