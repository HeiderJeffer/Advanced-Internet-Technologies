from django.urls import path, include
from django.contrib import admin
from secretsmodules import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('secretsmodules/', include('secretsmodules.urls')),
    # path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='index'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.LoginForm.as_view(), name='login'),
    path('', include('secretsmodules.urls')),
]
#if settings.DEBUG is True:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
