from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Rango says hey there world! <a href='/rango/about'>About</a> ")

def about(request):
    return HttpResponse("This tutorial has been put together by Naveen Mendis 2086839M <a href='/rango/'>Index</a>")