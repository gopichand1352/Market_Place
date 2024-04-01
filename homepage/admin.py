from django.contrib import admin
from homepage.models import Customer,Product,Cart,OrderPlaced

# Register your models here.

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer_name','phoneNumber',
                  'customer_locality','customer_city','customer_zipcode','customer_country','customer_state']

@admin.register(Product)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','pname','pcategory','pdescription','selling_price','discount_price','discount_percent','image1','image2','image3']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']

@admin.register(OrderPlaced)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity','price','order_id','razorpay_payment_id','amount_paid','ordered_date','status']


