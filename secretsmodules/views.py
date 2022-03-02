import json
import datetime
from decimal import *
from operator import itemgetter
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from . import forms
from . import models
from django.core import serializers
from secretsmodules.models import Secret, UserProfile, PurchasedItem, Cart
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout, get_user_model
import urllib
from django.conf import settings
from django.contrib import messages

# Create your views here.


def duplicate_mail(email):
    users = list(User.objects.filter(email = email))
    if len(users) > 0:
        return True
    return False

class HomePageView(ListView):
    template_name = 'secretsmodules/index.html'
    context_object_name = 'all_secrets'  #default: objectname_list
    ordering = ['-date']
    model = models.Secret

class DetailsView(DetailView):
    model = models.Secret
    template_name = 'secretsmodules/details.html'
    context_object_name = 'secret'    #default: objectname.

@login_required
def get_cart(request):
    cart = request.session.get('cart', dict())
    return render(request, 'secretsmodules/cart.html')

@login_required
def get_user_secrets(request):
    profile = UserProfile.objects.get(user=request.user)
    print(profile)
    purchased_items = Cart.objects.filter(user_id=profile.pk).values()
    user_purchased = list()
    # group by basket
    for value in purchased_items:
        item = PurchasedItem.objects.get(cart_id=value['id']).__dict__
        secret_dict = {"secret": Secret.objects.filter(pk=item['secret_id']).values()[0],
                       "purchase_date": value['purchase_date'], "pk": item['secret_id']}
        user_purchased.append(secret_dict)

    # sort by latest key
    user_purchased.sort(key=itemgetter('purchase_date'), reverse=True)
    return render(request, 'secretsmodules/user_secrets.html', context={'user_purchased': user_purchased})

@login_required
def add_to_cart(request, secret_id):
    if request.user.is_authenticated:
        cart = request.session.get('cart', dict())
        secret = Secret.objects.filter(pk=secret_id).values()[0]
        # if item already in cart
        if secret_id in cart:
            cart[secret_id]['quantity'] = cart[secret_id]['quantity'] + 1
        else:
            cart[secret_id] = {"secret": secret['title'], "quantity": 1, "price": float(secret['price'])}
        request.session['cart'] = cart
        return redirect('/cart')
    else:
        return HttpResponseRedirect(reverse('login'))

@login_required
def remove_from_cart(request, secret_id):
    cart = request.session.get('cart', dict())
    cart.pop(secret_id, None)
    request.session['cart'] = cart
    return redirect('/cart')

class CheckoutView(LoginRequiredMixin,TemplateView):
    def get(self, request, **kwargs):
        cart = request.session.get('cart', dict())
        total_order = 0
        profile = UserProfile.objects.get(user=request.user)
        balance = profile.balance
        for key in cart:
            total_order = total_order + (cart[key]['price'])
        return render(request, 'secretsmodules/checkout.html', context={"total_order": total_order, "balance": balance})
    def post(self, request, **kwargs):
        cart = request.session.get('cart')
        profile = UserProfile.objects.get(user=request.user)
        for key in cart:
            item_price = cart[key]['price']
            balance = float(profile.balance) - item_price
            if balance < 0:
                return
            else:
                secret = Secret.objects.get(pk=key)
                cart_item = Cart(user=profile, purchase_date=datetime.datetime.now())
                cart_item.save()
                purchased_item = PurchasedItem(cart=cart_item, secret=secret, purchased_price=item_price)
                purchased_item.save()
                profile.balance = Decimal(balance)
                profile.save()
        request.session['cart'] = dict()
        return render(request, 'secretsmodules/checkout_finished.html', context={"current_balance": profile.balance})




class RegisterForm(TemplateView):
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        form = forms.UserForm()
        return render(request, 'secretsmodules/register.html', context={'form': form})
    def post(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        form = forms.UserForm(request.POST)
        if form.is_valid():

            data = form.cleaned_data
            try:
                if duplicate_mail(data['email']):
                    form.add_error(field = 'email', error = "Email already in user")
                try:
                    validate_password(data['password'])
                except ValidationError as ve:
                    form.add_error(field = 'password', error = ve.messages)
                if len(form.errors) > 0:
                    return render(request, 'secretsmodules/register.html', context={'form': form})
                user = User.objects.create_user(username=data['username'],
                                             email=data['email'],
                                             password=data['password'],
                                             first_name = data['first_name'],
                                             last_name = data['last_name'])

            except IntegrityError as e:

                if 'unique constraint' in str(e).lower():
                    form.add_error(field = 'username', error="Username already in use")
                else:
                    form.add_error(field = none, error = "Unspecified error, try again later")
                return render(request, 'secretsmodules/register.html', context={'form': form})
            except Exception as e:
                form.add_error(field = None, error = "Unspecified Integrity error, try again later" )
                return render(request, 'secretsmodules/register.html', context={'form': form})
            try:
                profile = UserProfile(user = user, address = data['address'], phone = data['phone'], balance = 0)
                profile.save()
            except Exception as ex:
                print(ex)
            if profile.pk is None:
                user.delete()
                form.add_error(field = None, error = "Error registering, try again later." )
                return render(request, 'secretsmodules/register.html', context={'form': form})


            login(request=request,user=user)
            return HttpResponseRedirect(reverse('index'))   #change later to profile page
        else:
            return render(request, 'secretsmodules/register.html', context={'form': form})


class LoginForm(TemplateView):
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'secretsmodules/login.html')
    def post(self, request, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        botcarcher = request.POST.get('bctch')
        if len(botcarcher) > 0:
            return HttpResponse('Bot caught!') #here we must implement captcha
        failed_attemts = request.session.get("FailedLogin", 0)
        if failed_attemts >=3:
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            if result['success']:
                request.session["FailedLogin"] = 0
            elif failed_attemts == 3:
                request.session["FailedLogin"] +=1
                return render(request, 'secretsmodules/login.html', context={'captcha': True, "error":"user not found"})
            else:
                request.session["FailedLogin"] +=1
                return render(request, 'secretsmodules/login.html', context={'captcha': True, "error":"captcha validation failed"})
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request=request, user=user)

                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('User not active')
        else:
            if failed_attemts == 0:
                request.session["FailedLogin"] = 1
                return render(request, 'secretsmodules/login.html', context={"error":"user not found"})
            else:
                request.session["FailedLogin"] +=1
                return render(request, 'secretsmodules/login.html', context={"error":"user not found"})
            return HttpResponse('invalid login details')

class EditProfile(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):

        user_form = forms.UserEditForm(instance=request.user)
        profile_form = forms.ProfileEditForm(instance = request.user.profile)
        return render(request, 'secretsmodules/profile.html', context={'user_form': user_form, 'profile_form': profile_form})
    def post(self, request, **kwargs):
        my_context = dict()
        user_form = forms.UserEditForm(request.POST, instance=request.user)
        profile_form = forms.ProfileEditForm(request.POST, instance=request.user.profile)
        my_context['user_form'] = user_form
        my_context['profile_form'] = profile_form

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            my_context['success'] = True


        return render(request, 'secretsmodules/profile.html', context = my_context)



@login_required
def user_logout(request):
    logout(request)
    for sesskey in request.session.keys():
        del request.session[sesskey]
    return HttpResponseRedirect(reverse('index'))
