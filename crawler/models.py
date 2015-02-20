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
    dom = None
    p_url = None #pattern url object

    def __unicode__(self):
        return self.url

    def crawl(self, url):
		self.url = url

		self.p_url = URL(url)
		self.dom = DOM(self.p_url.download(cached=True))

		p = Predictor(self.p_url, self.dom)

		self.programming_language = p.predict_programming_language()


class SiteTechnologies(models.Model):
    site = models.OneToOneField(Site, related_name='site_technologies')
    webserver = models.CharField(max_length=50, blank=True)
    programming_language = models.CharField(max_length=50, blank=True)
    certificate = models.CharField(max_length=500, blank=True)
    certificate_authority = models.CharField(max_length=500, blank=True)
    html_version = models.CharField(max_length=500, blank=True)
