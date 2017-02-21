'''
This file contains the URL patterns for courses App
'''

from django.conf.urls import url, include
from courses.apis import router
from . import views

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^genre', views.get_genre),
    url(r'^course/(?P<id>[0-9]+)/$', views.get_course_by_id, name='course_by_id'),
    url(r'^menu', views.get_courses_for_menu)
]