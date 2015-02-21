from django.db import models
from pattern.web import URL, DOM, plaintext
from pattern.web import NODE, TEXT, COMMENT, ELEMENT, DOCUMENT
from predictor import Predictor

class SiteTechnologyManager(models.Manager):
    def _top(self, technology):
        return super(SiteTechnologyManager, self).get_queryset().values('value').annotate(count=models.Count(technology)).order_by('-count')[:10]

    def top_webservers(self):
        return self._top('webserver')

    def top_programming_languages(self):
        return self._top('programming_language')

class Location(models.Model):
    country = models.CharField(max_length=2)
    city = models.CharField(max_length=100, db_index=True)
    city_accent = models.CharField(max_length=100)
    region = models.CharField(max_length=10, null=True)
    population = models.IntegerField(default=0)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __unicode__(self):
        return "Country: %s, City: %s" % (self.country, self.city)


class Site(models.Model):
    url = models.CharField(max_length=500)
    ip_address = models.CharField(max_length=500)
    location = models.ForeignKey(Location, null=True, related_name='sites')
    company_name = models.CharField(max_length=500, blank=True)
    webserver = models.CharField(max_length=50, blank=True)
    programming_language = models.CharField(max_length=50, blank=True)
    certificate = models.CharField(max_length=500, blank=True)
    certificate_authority = models.CharField(max_length=500, blank=True)
    html_version = models.CharField(max_length=500, blank=True)
    frontend_language = models.CharField(max_length=500, blank=True)
    backend_framework = models.CharField(max_length=500, blank=True)
    frontend_framework = models.CharField(max_length=500, blank=True)
    logo_url = models.CharField(max_length=500, blank=True)

    #used for crawling and analyzing the website

    def __init__(self, *args, **kwargs):
        super(Site, self).__init__(*args, **kwargs)
        self.dom = None
        self.p_url = None  # pattern url object
        self.predictor = None


    def __unicode__(self):
        return self.url

    def crawl(self, url):
        self.url = url

        self.p_url = URL(url)
        self.dom = DOM(self.p_url.download(cached=True, unicode=True))

        self.predictor = Predictor(self.p_url, self.dom)

        self.predictor.predict_name()
        self.company_name = self.predictor.name

        self.predictor.predict_logo()
        self.logo_url = self.predictor.logo

        self.save()

        self.site_technologies.add(SiteTechnology(tech_type='webserver', value=self.predictor.get_webserver()))

        self.predictor.predict_programming_language()
        back_langs = []
        if self.predictor.backend_languages:
            for lang in self.predictor.backend_languages:
                back_langs.append(lang)
                self.site_technologies.add(SiteTechnology(tech_type='backend_language', value=lang))

        self.predictor.predict_frontend()
        front_langs = []
        if self.predictor.frontend_languages:
            for lang in self.predictor.frontend_languages:
                front_langs.append(lang)
                self.site_technologies.add(SiteTechnology(tech_type='frontend_language', value=lang))

        self.predictor.predict_frameworks()
        for lang in back_langs:
            bf = self.predictor.frameworks.get(self.programming_language, [])
            for f in bf:
                self.site_technologies.add(SiteTechnology(tech_type='backend_framework', value=f))
                
        for lang in front_langs:
            ff = self.predictor.frameworks.get(self.frontend_language, [])
            for f in ff:
                self.site_technologies.add(SiteTechnology(tech_type='frontend_framework', value=f))

        self.location = self.predictor.predict_location()

        self.save()

class SiteTechnology(models.Model):
    site = models.ForeignKey(Site, related_name='site_technologies')
    tech_type = models.CharField(max_length=500)
    value = models.CharField(max_length=500, blank=True)

    objects = SiteTechnologyManager()
