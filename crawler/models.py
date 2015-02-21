from django.db import models
from pattern.web import URL, DOM, plaintext
from pattern.web import NODE, TEXT, COMMENT, ELEMENT, DOCUMENT
from predictor import Predictor
from django.db import connection

class SiteTechnologyManager(models.Manager):
    def _top(self, technology):
        return super(SiteTechnologyManager, self).get_queryset().filter(tech_type=technology).values('value').annotate(count=models.Count('value')).order_by('-count')[:10]

    def top_technologies(self):
        return super(SiteTechnologyManager, self).get_queryset().values('value').annotate(count=models.Count('value')).order_by('-count')[:10]

    def top_webservers(self):
        return self._top('webserver')

    def top_programming_languages(self):
        return self._top('programming_language')

    def top_technologies_by_country(self, country):
        return super(SiteTechnologyManager, self).get_queryset().filter(site__location__country=country).values('value').annotate(count=models.Count('value')).order_by('-count')[:10]

    def top_technologies_by_countries(self):
        cursor = connection.cursor()
        #return super(SiteTechnologyManager, self).get_queryset().values('site__location__country', 'value').annotate(count=models.Count('value')).order_by('-count')[:10]
        cursor.execute(
            "SELECT country, value, COUNT(value) AS tech_count \
            FROM crawler_sitetechnology t INNER JOIN  \
                crawler_site s ON t.site_id = s.id INNER JOIN \
                crawler_location l ON s.location_id = l.id \
            GROUP BY country, value")
        return cursor.fetchall()
        


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
        webserver = self.predictor.get_webserver()

        #ORDER MATTERS!! DONT CHANGE THIS
        self.predictor.predict_programming_language()
        self.predictor.predict_frontend()
        self.predictor.predict_frameworks()
        self.predictor.predict_name()
        self.predictor.predict_logo()
        self.location = self.predictor.predict_location()
        #YOU CAN CHANGE AFTER THAT
        self.company_name = self.predictor.name
        self.logo_url = self.predictor.logo if self.predictor.logo else ""

        self.save()

        
        if webserver:
            self.site_technologies.add(SiteTechnology(tech_type='webserver', value=webserver))

        
        back_langs = []
        if self.predictor.backend_languages:
            for lang in self.predictor.backend_languages:
                back_langs.append(lang)
                self.site_technologies.add(SiteTechnology(tech_type='backend_language', value=lang))

        
        front_langs = []
        if self.predictor.frontend_languages:
            for lang in self.predictor.frontend_languages:
                front_langs.append(lang)
                self.site_technologies.add(SiteTechnology(tech_type='frontend_language', value=lang))

        
        for lang in back_langs:
            bf = self.predictor.frameworks.get(self.programming_language, [])
            for f in bf:
                self.site_technologies.add(SiteTechnology(tech_type='backend_framework', value=f))
                
        for lang in front_langs:
            ff = self.predictor.frameworks.get(self.frontend_language, [])
            for f in ff:
                self.site_technologies.add(SiteTechnology(tech_type='frontend_framework', value=f))


        self.save()

class SiteTechnology(models.Model):
    site = models.ForeignKey(Site, related_name='site_technologies')
    tech_type = models.CharField(max_length=500)
    value = models.CharField(max_length=500, blank=True)

    objects = SiteTechnologyManager()

    def __unicode__(self):
        return 'Type: %s, value: %s' % (self.tech_type, self.value)
