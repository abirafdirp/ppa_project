from django.conf.urls import include, url
from transaction import views
from django.contrib import admin

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli urls
    url(r'^$', views.display_today, name='today'),
    url(r'^saldodana$', views.display_saldodana, name='saldodana'),
    url(r'^(?P<day>[0-9]{2})/(?P<month>[0-9]{1,2})/(?P<year>[0-9]{4})/$',
        views.display_not_today, name='not-today'),
    url(r'^admin/', include(admin.site.urls)),
]
