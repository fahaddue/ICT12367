from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("ICT12367 SPU")
def about(request):
    return HttpResponse("Abount US")
def form(request):
    return render(request,'form.html')
def contact(request):
    return HttpResponse("fahad dueramae")

# Create your views here.
