from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

COUNTRY_CHOICES = (
    ('INDIA','INDIA'),
    ('USA','USA'),
    ('Canada','Canada'),
    ('France','France'),
)


STATE_CHOICES = (
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Telengana','Telengana'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Tamil Nadu','Tamil Nadu'),
) 


CATEGORY_CHOICES = (
    ('V','Vegetables'),
    ('F','Fruits'),
    ('S','Sweets'),
    ('BI','Bake Items'),
    ('SD','Soft Drinks'),
    ('MI','Milk Items'),
)


STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer_name=models.CharField(max_length=200)
    phoneNumber = PhoneNumberField(null=False, blank=False,max_length=12)
    customer_locality=models.CharField(max_length=200)
    customer_city=models.CharField(max_length=200)
    customer_zipcode=models.IntegerField()
    customer_country=models.CharField(choices=COUNTRY_CHOICES,max_length=50)
    customer_state=models.CharField(choices=STATE_CHOICES,max_length=50)

    def __str__(self):
        return str(self.id)
    
class Product(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    pname=models.CharField(max_length=100)
    pcategory=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    pdescription=models.TextField()
    selling_price=models.FloatField()
    discount_price=models.FloatField()
    discount_percent=models.IntegerField()
    image1=models.ImageField(upload_to='productimg')
    image2=models.ImageField(upload_to='productimg',blank=True,null=True)
    image3=models.ImageField(upload_to='productimg',blank=True,null=True)

    def __str__(self):
        return str(self.id)
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    price=models.FloatField()
    order_id=models.CharField(max_length=100,blank=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True)
    amount_paid=models.BooleanField(default=False)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='pending')

    def __str__(self):
        return str(self.id)


