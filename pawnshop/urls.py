
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('user_app.urls')),
    url(r'^', include('lot.urls')),
]

urlpatterns += staticfiles_urlpatterns()