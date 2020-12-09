from django.shortcuts import render, HttpResponse
from zipDownload import send_zipfile


def index(request):
    return render(request, 'dist/index.html')