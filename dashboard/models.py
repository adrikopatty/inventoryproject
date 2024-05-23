from django.db import models
#we import user order linked to user
from django.contrib.auth.models import  User

# Create your models here.
CATEGORY=(
    ('Stationary','Stationary'),
    ('Electronics','Electronics'),
    ('Food','Food'),
)
class Product(models.Model):
    name=models.CharField(max_length=100, null =True)
    category=models.CharField(max_length=20, choices=CATEGORY,null=True)
    quantity=models.PositiveIntegerField( null =True)
    #how to make look in the admin panel

    class Meta:
        verbose_name_plural = 'Product'

    

class Order(models.Model):
   product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
   staff = models.ForeignKey(User, models.CASCADE, null=True)  
   order_quantity= models.PositiveIntegerField(null= True)
   date = models.DateTimeField(auto_now_add=True)

   class Meta:
        verbose_name_plural = 'Order'
        
   def __str__ (self):
    product_str = str(self.product) if self.product else 'Unknown product'
    staff_str = self.staff.username if self.staff else 'Unknown staff'
    return f'{product_str} ordered by {staff_str}'
