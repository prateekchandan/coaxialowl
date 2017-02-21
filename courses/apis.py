'''
This file contains the Serialzers and routes for the APIs belonging to courses module
'''
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from courses.models import *

router = routers.DefaultRouter()

class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

router.register(r'genre', GenreViewSet)
