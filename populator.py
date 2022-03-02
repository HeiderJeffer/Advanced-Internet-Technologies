import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','secretsapp.settings')

import django

django.setup()

import random
import string
from secretsmodules.models import *
import csv
from faker import Faker
from django.contrib.auth.models import User
from django.core.files import File
import string
from django.db.models import Q
fakegen = Faker()

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def add_countries():
    dir = os.path.join(os.getcwd(),'tempdata','countries.csv')
    with open(dir,'r') as csvFile:
        reader = csv.reader(csvFile)
        next(reader,None)
        for row in reader:
            c = Country.objects.get_or_create(name = row[0], code = row[1])[0]


def add_secrets(n):
    countries = list(Country.objects.all())
    dir = os.path.join(os.getcwd(),'tempdata','images')

    images = [os.path.join(dir,x) for x in os.listdir(dir)]

    for i in range(0,n):
        title = fakegen.sentence()
        description = fakegen.text()
        price = float(random.randrange(500,10000))
        imagePath = images[random.randint(0,len(images)-1)] #I don't know how to save it programically, doing empty for now
        f = open(imagePath,'rb')
        img =File(f)
        date = fakegen.date_between(start_date="-1y", end_date="today")
        country = countries[random.randint(0,len(countries)-1)]
        rank = random.randint(1,5)
        secret = Secret.objects.get_or_create(title = title, description = description,
                                                price = price, date = date, country_of_origin = country, rank = rank)[0]
        secret.picture.save(random_string_generator(size = 32)+'.jpg',img,True)
        secret.save()

def add_users(n):
    for i in range(0,n):
        username = fakegen.user_name()
        email = fakegen.email()
        fname = fakegen.first_name()
        lname = fakegen.last_name()
        password = fakegen.word()
        addr = fakegen.address()
        phone = fakegen.phone_number()
        user = User.objects.create_user(username=username,
                                 email=email,
                                 password=password,
                                 first_name = fname,
                                 last_name = lname)
        user.save()
        profile = UserProfile(address = addr, phone = phone, user = user)
        profile.save()

def add_carts(n):
    users = list(UserProfile.objects.all())
    secrets = list(Secret.objects.all())
    for i in range(0,n):
        cart = Cart(user = users[random.randint(0,len(users)-1)])
        cart.save()
        for j in range(0, random.randint(1,5)):
            secret = secrets[random.randint(0, len(secrets)-1)]
            item = PurchasedItem(cart = cart, secret = secret, purchased_price = secret.price)
            item.save()
def replace_images(secrets):
    dir = os.path.join(os.getcwd(),'tempdata','images')
    images = [os.path.join(dir,x) for x in os.listdir(dir)]
    for item in secrets:
        imagePath = images[random.randint(0,len(images)-1)] #I don't know how to save it programically, doing empty for now
        f = open(imagePath,'rb')
        img =File(f)
        item.picture.save(random_string_generator(size = 32)+'.jpg',img,True)
        item.save()

if __name__ == '__main__':
    add_countries()
    add_secrets(30)
    add_users(8)
    add_carts(7)

    print('done')
