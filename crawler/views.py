from django.shortcuts import render
from crawler.models import Site, SiteTechnologies
from rest_framework import serializers, viewsets

class SiteTechnologiesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SiteTechnologies

class SiteSerializer(serializers.HyperlinkedModelSerializer):
    site_technologies = SiteTechnologiesSerializer(many=False, read_only=True)
    class Meta:
        model = Site
	fields = ('id', 'url', 'ip_address', 'location', 'company_name', 'site_technologies')

class SiteTechnologiesViewSet(viewsets.ModelViewSet):
    queryset = SiteTechnologies.objects.all()
    serializer_class = SiteTechnologiesSerializer

class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
