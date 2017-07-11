from django.conf.urls import include, url
from . import urls_apis, urls_views

urlpatterns = [
    url(r'^', include(urls_views)),
    url(r'^api/', include(urls_apis)),
]
