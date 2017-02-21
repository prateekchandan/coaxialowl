'''
Context Processors
'''
from datetime import date
from django.conf import settings
from courses.models import CourseMenu

def app_constants(request):
    '''
	return the value you want as a dictionary. you may add multiple values in there.
	'''
    menu = CourseMenu(name="menu")
    menu.add_all_courses()
    return {
        'MENU':menu.toDict(),
        'APP_NAME': settings.APP_NAME,
        'CURRENT_YEAR' : date.today().year
        }
