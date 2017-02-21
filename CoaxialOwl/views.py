'''
project wide views
'''
from django.shortcuts import render

def index(request):
    '''
    show home page
    '''
    return render(request, "home.html")
