from django.shortcuts import render
from crawler.models import Site, SiteTechnology, Location
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

class SiteTechnologySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SiteTechnology

class SiteSerializer(serializers.HyperlinkedModelSerializer):
    site_technologies = SiteTechnologySerializer(many=True, read_only=True)
    class Meta:
        model = Site

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    sites = SiteSerializer(many=True, read_only=True)
    class Meta:
        model = Location

class SiteTechnologyViewSet(viewsets.ModelViewSet):
    queryset = SiteTechnology.objects.all()
    serializer_class = SiteTechnologySerializer

class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class TopWebserversView(APIView):
    permission_classes = []

    def get(self, request, format=None):
	queryset = SiteTechnology.objects.top_webservers()
	return Response(queryset)

class TopTechnologiesByCountryView(APIView):
    permission_classes = []

    def get(self, request, country):
	queryset = SiteTechnology.objects.top_technologies_by_country(country)
	return Response(queryset)

class TopTechnologyView(APIView):
    permission_classes = []

    def get(self, request, technology):
	queryset = SiteTechnology.objects._top(technology)
	return Response(queryset)

class TopTechnologiesView(APIView):
    permission_classes = []

    def get(self, request):
	queryset = SiteTechnology.objects.top_technologies()
	return Response(queryset)

class TopTechnologiesByCountriesView(APIView):
    permission_classes = []

    def get(self, request):
	queryset = SiteTechnology.objects.top_technologies_by_countries()
	return Response(queryset)

class TopProgrammingLanguagesView(APIView):
    permission_classes = []

    def get(self, request, format=None):
	queryset = SiteTechnology.objects.top_programming_languages()
	return Response(queryset)

class SitesByCountryView(APIView):
    permission_classes = []

    def get(self, request, country):
	queryset = Site.objects.sites_by_country(country)
	return Response(SiteSerializer(queryset))
