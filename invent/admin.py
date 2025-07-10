from django.contrib import admin
from .models import InventoryItem, ItemRequest, StockTransaction # Import all your models

# Register your models here so they appear in the Django admin.
admin.site.register(InventoryItem)
admin.site.register(ItemRequest)
admin.site.register(StockTransaction)