from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # โยนหน้าทึ่จัดการ url ไปให้แอป services
    path('', include('services.urls')), 
]