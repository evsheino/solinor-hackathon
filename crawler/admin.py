from django.contrib import admin
from crawler.models import Site, SiteTechnology, Location

admin.site.register(Site)
admin.site.register(SiteTechnology)
admin.site.register(Location)
