from django.contrib import admin
from mainapp.models import ItemCategory, ParentCategory
from authapp.models import UserEmail, ShopUser

admin.site.register(UserEmail)
admin.site.register(ShopUser)
admin.site.register(ItemCategory)
admin.site.register(ParentCategory)
