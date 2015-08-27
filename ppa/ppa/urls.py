from django.conf.urls import include, url
from transaction import views
from django.contrib import admin

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli urls
    url(r'^$', views.display_today, name='today'),
    url(r'^admin/', include(admin.site.urls)),
]
