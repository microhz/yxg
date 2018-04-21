from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello zn")

def test_page(request) :
    return render(request, 'worker.html')

