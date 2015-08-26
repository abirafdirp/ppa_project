from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli urls
    url(r'^', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
]
