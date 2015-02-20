from django.conf.urls import patterns, include, url
from django.contrib import admin
from crawler.views import SiteViewSet, SiteTechnologiesViewSet, TopWebserversView, TopProgrammingLanguagesView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'sites', SiteViewSet)
router.register(r'site_technologies', SiteTechnologiesViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'solinorhackathon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^top_webservers/$', TopWebserversView.as_view(), name='topservers'),
    url(r'^top_programming_languages/$', TopProgrammingLanguagesView.as_view(), name='toplanguages'),
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
