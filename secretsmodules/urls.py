# howdy/urls.py
from django.urls import path
from django.urls import re_path
from secretsmodules import views
app_name = 'secretsmodules'

urlpatterns = [
    re_path(r'^details/(?P<pk>\d{1,50})/$', views.DetailsView.as_view(), name='details'),
    re_path(r'^add_to_cart/(?P<secret_id>[0-9]+)$', views.add_to_cart, name='add_to_cart'),
    re_path(r'^remove_from_cart/(?P<secret_id>[0-9]+)$', views.remove_from_cart, name='remove_from_cart'),
    re_path(r'^register/$', views.RegisterForm.as_view(), name='register'),
    path('cart/', views.get_cart, name='cart'),
    path('user_secrets/', views.get_user_secrets, name='user_secrets'),
    re_path(r'^checkout/$', views.CheckoutView.as_view(), name='checkout'),
    path('profile/', views.EditProfile.as_view(), name='profile'),
]
