from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path('products', views.products),
    path('feedback', views.feedback),
    path('form/', views.form, name='form'),
    path('edit/<int:person_id>/', views.edit, name='edit'),
    path('delete/<int:person_id>/', views.delete, name='delete'),
]