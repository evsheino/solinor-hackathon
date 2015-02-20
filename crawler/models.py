from django.db import models
from pattern.web import URL, DOM, plaintext
from pattern.web import NODE, TEXT, COMMENT, ELEMENT, DOCUMENT
from predictor import Predictor

class Site(models.Model):
    url = models.CharField(max_length=500)
    ip_address = models.CharField(max_length=500)
    location = models.CharField(max_length=100)
    company_name = models.CharField(max_length=500)
    webserver = models.CharField(max_length=50)
    programming_language = models.CharField(max_length=50)
    certificate = models.CharField(max_length=500)
    certificate_authority = models.CharField(max_length=500)
    html_version = models.CharField(max_length=500)

    #used for crawling and analyzing the website
    dom = None
    p_url = None #pattern url object

    def crawl(self, url):
		self.url = url

		self.p_url = URL(url)
		self.dom = DOM(self.p_url.download(cached=True))

		p = Predictor(self.p_url, self.dom)

		self.programming_language = p.predict_programming_language()




