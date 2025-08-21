from django.contrib import admin
from .models import Category, Location, Asset, Inventory, PurchaseOrder, Supplier

# Register your models here.


# Category
admin.site.register(Category)
# Location
admin.site.register(Location)
# Asset
admin.site.register(Asset)
# Inventory
admin.site.register(Inventory)
# PurchaseOrder
admin.site.register(PurchaseOrder)
# Supplier
admin.site.register(Supplier)