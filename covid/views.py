from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from covid.apicovid import *


import urllib
# Create your views here.


def utama(request):
    return render(request, 'index.html', {"region": GetRegion()["data"]})


def getRegion(request):
    dt = GetRegion()
    return JsonResponse(dt)


def getLastData(request, name="world"):
    dt = GetChart(name)
    return JsonResponse(dt)


def getPerRegion(request, name="world"):
    dt = GetRegionCity(name)
    return JsonResponse(dt)
