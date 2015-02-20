from django.db import models

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

