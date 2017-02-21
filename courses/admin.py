from django.contrib import admin
from .models import Genre, Class, CourseType, Course, Subject, GraduationDepartment

admin.site.register(Genre)
admin.site.register(Class)
admin.site.register(CourseType)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(GraduationDepartment)
