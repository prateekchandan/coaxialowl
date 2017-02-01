from django.conf import settings # import the settings file
from datetime import date

def app_constants(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {
    			'APP_NAME': settings.APP_NAME,
    			'CURRENT_YEAR' : date.today().year
    		}