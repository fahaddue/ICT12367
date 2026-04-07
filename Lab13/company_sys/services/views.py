from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from .models import Person
from django.db.models import Q

def index(request):
    all_person = Person.objects.all()  
    return render(request,"index.html",{"all_person":all_person})
def products(request):
    return render(request,"products.html")
def feedback(request):
    return render(request,'feedback.html')

def form(request):
    if request.method == "POST":
        # รับข้อมูลจากฟอร์ม
        name = request.POST.get("name")
        age = request.POST.get("age")

        # บันทึกข้อมูลลงฐานข้อมูล
        person = Person.objects.create(
            name = name,
            age = age
        )

        # เปลี่ยนเส้นทางไปหน้าแรก
        return redirect("/")
    else:
        # แสดงฟอร์ม
        return render(request, "form.html")
    
def edit(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    if request.method == "POST":
        # รับข้อมูลจากฟอร์ม
        name = request.POST.get("name")
        age = request.POST.get("age")

        # บันทึกข้อมูลลงฐานข้อมูล
        person.name = name
        person.age = age
        person.save()

        # เปลี่ยนเส้นทางไปหน้าแรก
        return redirect("/")
    else:
        # แสดงฟอร์ม
        return render(request, "edit.html", {"person": person})

def delete(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    person.delete()
    return redirect("/")


from django.db.models import Q  # อย่าลืม import Q มาไว้ด้านบนสุดของไฟล์ด้วยนะครับ

def index(request):
    # 1. ดึงข้อมูลทั้งหมดมาก่อน
    all_Person = Person.objects.all()
    
    # 2. รับค่าจากช่องค้นหา
    query = request.GET.get('q')
    
    # 3. ตรวจสอบและกรองข้อมูล (จุดที่ต้องแก้)
    if query:
        # ใช้เครื่องหมาย | เพื่อแทนคำว่า "หรือ"
        all_Person = all_Person.filter(Q(name__icontains=query) | Q(age__icontains=query))
    
    # 4. ส่งข้อมูลไปที่หน้าเว็บ
    return render(request, "index.html", {"all_person": all_Person})