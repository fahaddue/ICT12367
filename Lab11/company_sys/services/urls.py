from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path('products', views.products),
    path('feedback', views.feedback),
]