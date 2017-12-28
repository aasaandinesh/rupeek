from django.shortcuts import render

# Create your views here.
from django.views import View


class MainView(View):
    def get(self,request):
        return "Hello World"
