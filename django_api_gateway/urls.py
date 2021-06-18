from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from gateway import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^{}(\d+)/$'.format(settings.PROXY_PATH), views.router_page),
    url(r'aaa'.format(settings.PROXY_PATH), views.test),
]

from django.conf import settings
from django.urls import include, path  # For django versions from 2.0 and up

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
