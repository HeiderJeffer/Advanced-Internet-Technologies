from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
# Create your models here.

class Country(models.Model):

    name = models.CharField(max_length = 150, unique = True)
    code = models.CharField(max_length = 2, unique = True)


class Secret(models.Model):

    title = models.CharField(max_length = 264, unique = False)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    picture = models.ImageField(upload_to = 'secret_pics',blank = True)
    date = models.DateField()
    country_of_origin = models.ForeignKey('Country',on_delete=models.PROTECT)
    rank = models.IntegerField()


class UserProfile(models.Model):
    #username, password, first and last name and email are included in djangos user class

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'profile')
    address = models.CharField(max_length = 264, unique = False, blank = True)
    phone = models.CharField(max_length = 20,  blank = True)
    balance = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('10000.00'))


class Cart(models.Model):

    user = models.ForeignKey('UserProfile', on_delete=models.PROTECT)
    purchase_date = models.DateTimeField( auto_now_add = True)


class PurchasedItem(models.Model):

    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    secret = models.ForeignKey('Secret', on_delete=models.CASCADE)
    purchased_price = models.DecimalField(decimal_places=2, max_digits=10)
