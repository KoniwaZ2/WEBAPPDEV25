from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def name(request):
    return HttpResponse("Victor Marlino")

def school(request):
    return HttpResponse("Prasmul!")