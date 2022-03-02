from django.conf.urls import url, include
from django.contrib import admin
from secretsmodules import views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # url(r'^secretsmodules/', include('secretsmodules.urls')),
    #url(r'^admin/', admin.site.urls),
    url(r'^$', views.HomePageView.as_view(), name = 'index'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^login/$', views.LoginForm.as_view(), name='login'),
    url(r'^', include('secretsmodules.urls')),
]
#if settings.DEBUG is True:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
