from django.contrib import admin

from secretsmodules.models import Country, UserProfile, Cart, Secret, PurchasedItem
# Register your models here.

admin.site.register(Country)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(Secret)
admin.site.register(PurchasedItem)
