# howdy/urls.py
from django.urls import path
from django.conf.urls import url
from secretsmodules import views


app_name = 'secretsmodules'
urlpatterns = [
    url(r'^details/(?P<pk>\d{1,50})/$',views.DetailsView.as_view(), name = 'details'),
    url(r'^add_to_cart/(?P<secret_id>[0-9]+)$', views.add_to_cart, name='add_to_cart'),
    url(r'^remove_from_cart/(?P<secret_id>[0-9]+)$', views.remove_from_cart, name='remove_from_cart'),
    url(r'^register/$',views.RegisterForm.as_view(), name='register'),
    url('cart/', views.get_cart, name='cart'),
    url('user_secrets/', views.get_user_secrets, name='user_secrets'),
    url(r'^checkout/$', views.CheckoutView.as_view(), name='checkout'),
    path('profile/',views.EditProfile.as_view(), name = 'profile'),
]
