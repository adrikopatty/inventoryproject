from django.contrib import admin
from.models import Product,Order
from django.contrib.auth.models import Group
#changing admin page title
admin.site.site_header = "Patty's Inventory Dashboard"

# to change display-makes it appear in table format and w eadd product admin to the register moder as a parameter
class ProductAdmin (admin.ModelAdmin):
    list_display = ('name','quantity','category')
    #helpa as filter by category
    list_filter=['category']

# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(Order)


#this how they unegister a model/import it
#admin.site.unregister(Group)