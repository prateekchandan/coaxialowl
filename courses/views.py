'''
Views
'''
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404, HttpResponse
from courses.apis import GenreViewSet
from courses.models import CourseMenu, Course, Subject
import json

def get_courses_for_menu(request):
    '''
    Get the Course List To show in Menu IN JSON Format
    '''
    menu = CourseMenu(name="menu")
    menu.add_all_courses()
    return JsonResponse(menu.toDict(), safe=False)

def get_genre(request):
    '''
    Get genre in json
    '''
    genre = GenreViewSet.as_view({'get': 'list'})(request).data
    return JsonResponse(genre, safe=False)

def get_course_by_id(request, id):
    course = get_object_or_404(Course, id=id)
    subjects = Subject.objects.filter(course_id=course.id)
    return render(request, 'courses/CourseId.html', {'course':course, 'subjects':subjects})
