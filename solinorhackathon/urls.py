from django.conf.urls import patterns, include, url
from django.contrib import admin
from crawler.views import SiteViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'sites', SiteViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'solinorhackathon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
