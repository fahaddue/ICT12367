from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request,"index.html")
def about(request):
    return render("Abount US")
def form(request):
    return render(request,'form.html')
def about(request):
    return render(request,'about.html')
# Create your views here.
