from django.shortcuts import render
from .services import *

# Create your views here.
def HomeView(request):
    return render(request,'index.html')

