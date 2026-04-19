import os
from django.db import models
from datetime import datetime

def get_slip_path(instance, filename):
    folder_name = datetime.now().strftime('%B%Y')
    return os.path.join('img_slip', folder_name, filename)

class Admin(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, default='staff')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'admins'

class Tenant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    id_card_no = models.CharField(max_length=13, unique=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    address = models.TextField()
    
    notify_email = models.BooleanField(default=True)
    notify_line = models.BooleanField(default=False)
    sync_calendar = models.BooleanField(default=False)
    calendar_email = models.EmailField(max_length=254, null=True, blank=True)

    class Meta:
        db_table = 'tenants'

class RoomType(models.Model):
    name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'room_types'

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    floor = models.IntegerField()
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='available')

    class Meta:
        db_table = 'rooms'

class Contract(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) 
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    
    is_signed = models.BooleanField(default=False)
    signature_data = models.TextField(null=True, blank=True)
    signature_type = models.CharField(max_length=20, null=True, blank=True)
    signed_at = models.DateTimeField(null=True, blank=True)

    # --- ฟิลด์ใหม่สำหรับการพิมพ์รายละเอียดในสัญญา ---
    made_at = models.CharField(max_length=255, null=True, blank=True)
    advance_payment_months = models.IntegerField(default=1)
    rent_due_day = models.IntegerField(default=5)
    witness_1 = models.CharField(max_length=150, null=True, blank=True)
    witness_2 = models.CharField(max_length=150, null=True, blank=True)

    # --- ฟิลด์ใหม่สำหรับการแจ้งยกเลิกสัญญาเช่าล่วงหน้า ---
    is_cancel_requested = models.BooleanField(default=False)
    cancel_effective_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'contracts'

class Invoice(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    invoice_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    room_charge = models.DecimalField(max_digits=10, decimal_places=2)
    water_charge = models.DecimalField(max_digits=10, decimal_places=2)
    electricity_charge = models.DecimalField(max_digits=10, decimal_places=2)
    other_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    class Meta:
        db_table = 'invoices'

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'โอนเงินบัญชีธนาคาร'),
        ('cash', 'เงินสด'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'รอยืนยัน'),
        ('verified', 'ยืนยันแล้ว'),
        ('rejected', 'ปฏิเสธ'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='bank_transfer')
    
    slip_image_url = models.FileField(upload_to=get_slip_path, max_length=255, db_column='slip_image_url', null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    note = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'payments'

class MaintenanceRequest(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    repair_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    admin_remark = models.TextField(null=True, blank=True) 

    class Meta:
        db_table = 'maintenance_requests'

class SystemInfo(models.Model):
    short_name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    description = models.CharField(max_length=50)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    tax_id = models.CharField(max_length=20, null=True, blank=True)
    water_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    electricity_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    promptpay_no = models.CharField(max_length=20, null=True, blank=True)
    promptpay_name = models.CharField(max_length=100, null=True, blank=True)
    system_version = models.CharField(max_length=20, default='1.0.0')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'system_info'

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj
    
class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [('car', 'รถยนต์'), ('motorcycle', 'รถจักรยานยนต์'), ('other', 'อื่นๆ')]
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='vehicles')
    license_plate = models.CharField(max_length=20)
    province = models.CharField(max_length=50)
    brand = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=20, null=True, blank=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES, default='car')
    note = models.TextField(null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vehicles'