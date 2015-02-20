from django.shortcuts import render
from crawler.models import Site
from rest_framework import serializers, viewsets

class SiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Site

class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
