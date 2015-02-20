from django.db import models
from pattern.web import URL, DOM, plaintext
from pattern.web import NODE, TEXT, COMMENT, ELEMENT, DOCUMENT
from predictor import Predictor


class Site(models.Model):
    url = models.CharField(max_length=500)
    ip_address = models.CharField(max_length=500)
    location = models.CharField(max_length=100, blank=True)
    company_name = models.CharField(max_length=500, blank=True)

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

        self.webserver = self.predictor.get_webserver()
        self.predictor.predict_programming_language()
        self.predictor.predict_frontend()
        self.predictor.predict_name()
        self.predictor.predict_logo()



class SiteTechnologies(models.Model):
    site = models.OneToOneField(Site, related_name='site_technologies')
    webserver = models.CharField(max_length=50, blank=True)
    programming_language = models.CharField(max_length=50, blank=True)
    certificate = models.CharField(max_length=500, blank=True)
    certificate_authority = models.CharField(max_length=500, blank=True)
    html_version = models.CharField(max_length=500, blank=True)
