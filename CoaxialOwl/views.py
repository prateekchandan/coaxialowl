from django.http import HttpResponse
from django.shortcuts import render
import json

def index(request):
	ctx = {}
	ctx["error"] = 404
	ctx["message"] = "URL Not Found"
	#return HttpResponse("<h1>Hello World</h1>")
	return render(request, "home.html", {"name" : "CoaxialOwl"})