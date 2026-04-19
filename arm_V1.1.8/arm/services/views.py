from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from datetime import datetime, date, timedelta
from django.conf import settings

# Import models ทั้งหมดที่ต้องการใช้ รวมถึง Payment ให้เพิ่มต่อท้ายเข้าไป
from .models import Tenant, Contract, Admin, Invoice, MaintenanceRequest, SystemInfo, Room, RoomType, Vehicle, Payment

@require_POST
def tenant_edit(request, tenant_id):
    if not request.session.get('admin_id'):
        return redirect('index_login')
    try:
        tenant = Tenant.objects.get(id=tenant_id)
        tenant.first_name = request.POST.get('first_name', '').strip()
        tenant.last_name = request.POST.get('last_name', '').strip()
        tenant.phone = request.POST.get('phone', '').strip()
        tenant.email = request.POST.get('email', '').strip()
        tenant.address = request.POST.get('address', '').strip()
        tenant.save()
        messages.success(request, f'อัปเดตข้อมูลผู้เช่าคุณ {tenant.first_name} เรียบร้อยแล้ว')
    except Tenant.DoesNotExist:
        messages.error(request, 'ไม่พบข้อมูลผู้เช่าในระบบ')
    return redirect('tenant')


@require_POST
def vehicle_add(request, tenant_id):
    if not request.session.get('admin_id'):
        return redirect('index_login')
    try:
        tenant = Tenant.objects.get(id=tenant_id)
        Vehicle.objects.create(
            tenant=tenant,
            vehicle_type=request.POST.get('vehicle_type', 'car'),
            license_plate=request.POST.get('license_plate', '').strip(),
            province=request.POST.get('province', '').strip(),
            brand=request.POST.get('brand', '').strip(),
            color=request.POST.get('color', '').strip(),
            note=request.POST.get('note', '').strip()
        )
        messages.success(request, 'เพิ่มข้อมูลยานพาหนะใหม่เรียบร้อยแล้ว')
    except Tenant.DoesNotExist:
        messages.error(request, 'ไม่พบผู้เช่าในระบบ')
    except Exception as e:
        messages.error(request, f'เกิดข้อผิดพลาด: {str(e)}')
    return redirect('tenant')


@require_POST
def vehicle_delete(request, vehicle_id):
    if not request.session.get('admin_id'):
        return redirect('index_login')
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
        plate = vehicle.license_plate
        vehicle.delete()
        messages.success(request, f'ลบข้อมูลรถทะเบียน {plate} ออกจากระบบแล้ว')
    except Vehicle.DoesNotExist:
        messages.error(request, 'ไม่พบข้อมูลรถยนต์คันนี้')
    return redirect('tenant')


ROOM_STATUS_CHOICES = ('available', 'occupied', 'maintenance')
MAINTENANCE_STATUS_CHOICES = ('new', 'in_progress', 'completed')

def system_info_context(request):
    return {'system_info': SystemInfo.get_settings()}

def contract_detail(request, contract_id):
    """หน้าดูรายละเอียดสัญญาเช่า (เข้าได้ทั้งแอดมินและลูกบ้าน)"""
    tenant_id = request.session.get('tenant_id')
    admin_id = request.session.get('admin_id')

    if not tenant_id and not admin_id:
        return redirect('index_login')

    try:
        contract = Contract.objects.select_related('tenant', 'room', 'room__room_type').get(id=contract_id)
    except Contract.DoesNotExist:
        messages.error(request, 'ไม่พบสัญญาเช่าที่ระบุ')
        return redirect('dashboard' if tenant_id else 'main')

    if tenant_id and contract.tenant_id != tenant_id:
        messages.error(request, 'คุณไม่มีสิทธิ์เข้าถึงสัญญานี้')
        return redirect('dashboard')

    system_info = SystemInfo.get_settings()
    return render(request, 'contract.html', {
        'contract': contract,
        'tenant': contract.tenant,
        'system_info': system_info
    })

@require_POST
def contract_sign(request, contract_id):
    """ระบบบันทึกลายเซ็นจากลูกบ้าน"""
    tenant_id = request.session.get('tenant_id')
    if not tenant_id:
        return redirect('index_login')

    try:
        contract = Contract.objects.get(id=contract_id, tenant_id=tenant_id)

        if contract.is_signed:
            messages.warning(request, 'สัญญานี้ถูกลงนามและมีผลบังคับใช้ไปแล้ว')
        else:
            signature_type = request.POST.get('signature_type', 'type')
            signature_data = request.POST.get('signature_data', '')

            if signature_data:
                contract.is_signed = True
                contract.signature_type = signature_type
                contract.signature_data = signature_data
                contract.signed_at = datetime.now()
                contract.save()
                messages.success(request, 'บันทึกลายมือชื่อและยอมรับสัญญาเรียบร้อยแล้ว')

    except Contract.DoesNotExist:
        messages.error(request, 'ไม่พบสัญญาเช่าของคุณ')

    return redirect('contract_detail', contract_id=contract_id)

def index_login(request):
    if request.session.get('tenant_id'):
        return redirect('dashboard')
    if request.session.get('admin_id'):
        return redirect('main')

    if request.method == 'POST':
        login_type = request.POST.get('login_type', 'tenant')

        if login_type == 'tenant':
            id_card = request.POST.get('id_card_no', '').strip()
            phone = request.POST.get('phone', '').strip()
            try:
                tenant = Tenant.objects.get(id_card_no=id_card, phone=phone)
                request.session['tenant_id'] = tenant.id
                messages.success(request, 'login_success')
                return redirect('dashboard')
            except Tenant.DoesNotExist:
                return render(request, 'index.html', {
                    'error': "เลขบัตรประชาชนหรือเบอร์โทรศัพท์ไม่ถูกต้อง",
                    'active_mode': 'tenant'
                })

        elif login_type == 'admin':
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            try:
                admin_user = Admin.objects.get(username=username, is_active=True)
                if 'example_hash' in admin_user.password_hash and password == '1234':
                    admin_user.password_hash = make_password('1234')
                    admin_user.save()

                if check_password(password, admin_user.password_hash):
                    request.session['admin_id'] = admin_user.id
                    request.session['admin_role'] = admin_user.role
                    request.session['admin_name'] = f"{admin_user.first_name} {admin_user.last_name}"
                    messages.success(request, 'login_success')
                    return redirect('main')
                else:
                    return render(request, 'index.html', {
                        'error': "รหัสผ่านไม่ถูกต้อง",
                        'active_mode': 'admin'
                    })
            except Admin.DoesNotExist:
                return render(request, 'index.html', {
                    'error': "ไม่พบชื่อผู้ใช้งานนี้ หรือบัญชีถูกระงับ",
                    'active_mode': 'admin'
                })
    return render(request, 'index.html', {'active_mode': 'tenant'})


def dashboard(request):
    tenant_id = request.session.get('tenant_id')
    if not tenant_id:
        return redirect('index_login')
        
    try:
        tenant = Tenant.objects.prefetch_related('vehicles').get(id=tenant_id)
        active_contract = Contract.objects.filter(tenant=tenant, is_active=True).select_related('room', 'room__room_type').first()
        
        invoices = []
        unpaid_count = 0
        if active_contract:
            invoices_qs = Invoice.objects.filter(contract=active_contract).order_by('-due_date')
            unpaid_count = invoices_qs.filter(is_paid=False).count()
            
            invoices = list(invoices_qs)
            for inv in invoices:
                inv.latest_payment = Payment.objects.filter(invoice=inv).last()
                
        maintenance_requests = MaintenanceRequest.objects.filter(tenant=tenant).order_by('-created_at')
        system_info = SystemInfo.get_settings()

        return render(request, 'dashboard.html', {
            'tenant': tenant,
            'active_contract': active_contract,
            'invoices': invoices,
            'unpaid_count': unpaid_count,
            'maintenance_requests': maintenance_requests,
            'system_info': system_info
        })
    except Tenant.DoesNotExist:
        return redirect('tenant_logout')
    
def tenant_logout(request):
    if 'tenant_id' in request.session:
        del request.session['tenant_id']
    return redirect('index_login')

# --- ระบบของ Admin ---
def main(request):
    admin_id = request.session.get('admin_id')
    if not admin_id: return redirect('index_login')
    
    try:
        admin = Admin.objects.get(id=admin_id)

        # --- ตรวจสอบสัญญาที่มีการแจ้งยกเลิกและถึงกำหนดปลดห้องอัตโนมัติ ---
        today = date.today()
        expiring_contracts = Contract.objects.filter(is_active=True, is_cancel_requested=True, cancel_effective_date__lte=today)
        for c in expiring_contracts:
            # ปิดสัญญา
            c.is_active = False
            c.end_date = today # ใส่วันที่สิ้นสุดจริงเป็นวันนี้
            c.save()
            # คืนสถานะห้องให้เป็นว่าง
            room = c.room
            room.status = 'available'
            room.save()
        # -------------------------------------------------------------

        contracts_qs = Contract.objects.all().select_related('tenant', 'room', 'room__room_type').order_by('-is_active', '-id')
        contracts_paginator = Paginator(contracts_qs, 10)
        contracts = contracts_paginator.get_page(request.GET.get('page'))

        rooms_qs = Room.objects.select_related('room_type').order_by('floor', 'room_number')
        rooms_paginator = Paginator(rooms_qs, 10)
        rooms = rooms_paginator.get_page(request.GET.get('room_page'))

        room_types = RoomType.objects.all().order_by('name')
        all_room_numbers = list(Room.objects.values_list('room_number', flat=True))

        # สรุปสถานะห้องพัก (การ์ดแสดงสถานะ)
        room_total = Room.objects.count()
        room_available = Room.objects.filter(status='available').count()
        room_occupied = Room.objects.filter(status='occupied').count()
        room_maintenance = Room.objects.filter(status='maintenance').count()

        # สรุปสถานะสัญญาเช่า (การ์ดแสดงสถานะ)
        contract_total = Contract.objects.count()
        contract_active = Contract.objects.filter(is_active=True, is_cancel_requested=False).count()
        contract_cancel_requested = Contract.objects.filter(is_active=True, is_cancel_requested=True).count()
        contract_inactive = Contract.objects.filter(is_active=False).count()

        return render(request, 'main.html', {
            'admin': admin,
            'contracts': contracts,
            'rooms': rooms,
            'room_types': room_types,
            'all_room_numbers': all_room_numbers,
            'room_total': room_total,
            'room_available': room_available,
            'room_occupied': room_occupied,
            'room_maintenance': room_maintenance,
            'contract_total': contract_total,
            'contract_active': contract_active,
            'contract_cancel_requested': contract_cancel_requested,
            'contract_inactive': contract_inactive,
        })
    except Admin.DoesNotExist:
        return redirect('admin_logout')

@require_POST
def room_add(request):
    if not request.session.get('admin_id'): return redirect('index_login')
    room_number = request.POST.get('room_number', '').strip()
    floor_raw = request.POST.get('floor', '').strip()
    room_type_id = request.POST.get('room_type_id', '').strip()
    status = request.POST.get('status', 'available').strip()

    if not room_number or not floor_raw or not room_type_id:
        messages.error(request, 'กรุณากรอกข้อมูลให้ครบถ้วน')
        return redirect('main')

    try:
        floor = int(floor_raw)
    except ValueError:
        messages.error(request, 'ชั้นต้องเป็นตัวเลข')
        return redirect('main')

    if Room.objects.filter(room_number=room_number).exists():
        messages.error(request, f'เลขห้อง {room_number} มีอยู่ในระบบแล้ว')
        return redirect('main')

    try:
        room_type = RoomType.objects.get(id=room_type_id)
    except RoomType.DoesNotExist:
        messages.error(request, 'ไม่พบประเภทห้องที่เลือก')
        return redirect('main')

    Room.objects.create(room_number=room_number, floor=floor, room_type=room_type, status=status if status in ROOM_STATUS_CHOICES else 'available')
    messages.success(request, f'เพิ่มห้องพัก {room_number} เรียบร้อยแล้ว')
    return redirect('main')


@require_POST
def room_edit(request, room_id):
    if not request.session.get('admin_id'): return redirect('index_login')
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        messages.error(request, 'ไม่พบข้อมูลห้องพักที่ต้องการแก้ไข')
        return redirect('main')

    room_number = request.POST.get('room_number', '').strip()
    floor_raw = request.POST.get('floor', '').strip()
    room_type_id = request.POST.get('room_type_id', '').strip()
    status = request.POST.get('status', '').strip()

    if not room_number or not floor_raw or not room_type_id:
        messages.error(request, 'กรุณากรอกข้อมูลให้ครบถ้วน')
        return redirect('main')

    try:
        floor = int(floor_raw)
    except ValueError:
        messages.error(request, 'ชั้นต้องเป็นตัวเลข')
        return redirect('main')

    if Room.objects.filter(room_number=room_number).exclude(id=room_id).exists():
        messages.error(request, f'เลขห้อง {room_number} มีอยู่ในระบบแล้ว')
        return redirect('main')

    try:
        room_type = RoomType.objects.get(id=room_type_id)
    except RoomType.DoesNotExist:
        messages.error(request, 'ไม่พบประเภทห้องที่เลือก')
        return redirect('main')

    room.room_number = room_number
    room.floor = floor
    room.room_type = room_type
    if status in ROOM_STATUS_CHOICES: room.status = status
    room.save()
    messages.success(request, f'อัปเดตห้องพัก {room_number} เรียบร้อยแล้ว')
    return redirect('main')

@require_POST
def contract_edit(request, contract_id):
    if not request.session.get('admin_id'): return redirect('index_login')
    try:
        contract_obj = Contract.objects.select_related('tenant').get(id=contract_id)
    except Contract.DoesNotExist:
        messages.error(request, 'ไม่พบสัญญาเช่าที่ต้องการแก้ไข')
        return redirect('main')

    tenant_name = request.POST.get('tenant_name', '').strip()
    id_card_no = request.POST.get('id_card_no', '').strip()
    start_date = request.POST.get('start_date', '').strip()
    end_date = request.POST.get('end_date', '').strip()
    deposit_raw = request.POST.get('deposit', '').strip()
    is_active_raw = request.POST.get('is_active', '').strip()

    if not tenant_name or not id_card_no or not start_date or not deposit_raw:
        messages.error(request, 'กรุณากรอกข้อมูลให้ครบถ้วน')
        return redirect('main')

    try:
        deposit = Decimal(deposit_raw)
    except (InvalidOperation, ValueError):
        messages.error(request, 'เงินประกันต้องเป็นตัวเลข')
        return redirect('main')

    if Tenant.objects.filter(id_card_no=id_card_no).exclude(id=contract_obj.tenant_id).exists():
        messages.error(request, f'เลขบัตรประชาชน {id_card_no} ถูกใช้โดยผู้เช่ารายอื่นแล้ว')
        return redirect('main')

    first_name, _, last_name = tenant_name.partition(' ')
    tenant_obj = contract_obj.tenant
    tenant_obj.first_name = first_name
    tenant_obj.last_name = last_name
    tenant_obj.id_card_no = id_card_no
    tenant_obj.save()

    contract_obj.start_date = start_date
    contract_obj.end_date = end_date or None
    contract_obj.deposit = deposit
    
    # กรณีแอดมินปิดสัญญาเองด้วยมือ (เปลี่ยนจากปกติเป็นสิ้นสุด)
    was_active = contract_obj.is_active
    new_is_active = (is_active_raw == 'True')
    
    contract_obj.is_active = new_is_active
    contract_obj.save()
    
    # ถ้าปิดสัญญา ให้เปลี่ยนสถานะห้องเป็นว่างด้วย
    if was_active and not new_is_active:
        room = contract_obj.room
        room.status = 'available'
        room.save()

    messages.success(request, f'อัปเดตสัญญาเช่าห้อง {contract_obj.room.room_number} เรียบร้อยแล้ว')
    return redirect('main')

@require_POST
def maintenance_update(request, request_id):
    if not request.session.get('admin_id'): return redirect('index_login')
    try:
        repair = MaintenanceRequest.objects.get(id=request_id)
    except MaintenanceRequest.DoesNotExist:
        messages.error(request, 'ไม่พบรายการแจ้งซ่อมที่ต้องการอัปเดต')
        return redirect('maintenance')

    status = request.POST.get('status', '').strip()
    repair_cost_str = request.POST.get('repair_cost', '0').strip()
    admin_remark = request.POST.get('admin_remark', '').strip()

    if status not in MAINTENANCE_STATUS_CHOICES:
        messages.error(request, 'สถานะที่เลือกไม่ถูกต้อง')
        return redirect('maintenance')

    try:
        repair.repair_cost = Decimal(repair_cost_str) if repair_cost_str else Decimal('0.00')
    except (InvalidOperation, ValueError):
        messages.error(request, 'ค่าใช้จ่ายต้องเป็นตัวเลข')
        return redirect('maintenance')

    repair.status = status
    repair.admin_remark = admin_remark
    repair.save()
    messages.success(request, f'บันทึกข้อมูลการแจ้งซ่อมห้อง {repair.room.room_number} สำเร็จ')
    return redirect('maintenance')

@require_POST
def room_delete(request, room_id):
    if not request.session.get('admin_id'): return redirect('index_login')
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        messages.error(request, 'ไม่พบข้อมูลห้องพักที่ต้องการลบ')
        return redirect('main')

    if Contract.objects.filter(room=room).exists():
        messages.error(request, f'ไม่สามารถลบห้อง {room.room_number} ได้ เนื่องจากมีสัญญาเช่าผูกกับห้องนี้อยู่')
        return redirect('main')

    room_number = room.room_number
    room.delete()
    messages.success(request, f'ลบห้องพัก {room_number} เรียบร้อยแล้ว')
    return redirect('main')

def tenant(request):
    admin_id = request.session.get('admin_id')
    if not admin_id: return redirect('index_login')
    
    try:
        admin = Admin.objects.get(id=admin_id)
        tenants_qs = Tenant.objects.prefetch_related('vehicles').all()
        paginator = Paginator(tenants_qs, 10)
        tenants_data = paginator.get_page(request.GET.get('page'))

        total_cars = Vehicle.objects.filter(vehicle_type='car').count()
        total_motorcycles = Vehicle.objects.filter(vehicle_type='motorcycle').count()

        return render(request, 'tenant.html', {
            'admin': admin,
            'tenants': tenants_data,
            'total_cars': total_cars,
            'total_motorcycles': total_motorcycles
        })
    except Admin.DoesNotExist:
        return redirect('admin_logout')

def maintenance(request):
    admin_id = request.session.get('admin_id')
    if not admin_id: return redirect('index_login')
    
    admin = Admin.objects.get(id=admin_id)
    requests_qs = MaintenanceRequest.objects.select_related('room', 'tenant').all()
    count_pending    = requests_qs.filter(status='pending').count()
    count_in_progress = requests_qs.filter(status='in_progress').count()
    count_completed  = requests_qs.filter(status='completed').count()
    paginator = Paginator(requests_qs, 10)
    requests = paginator.get_page(request.GET.get('page'))
    return render(request, 'maintenance.html', {
        'admin': admin,
        'requests': requests,
        'count_pending': count_pending,
        'count_in_progress': count_in_progress,
        'count_completed': count_completed,
    })

def config(request):
    admin_id = request.session.get('admin_id')
    if not admin_id: return redirect('index_login')
    admin = Admin.objects.get(id=admin_id)
    return render(request, 'config.html', {'admin': admin})

def admin_logout(request):
    if 'admin_id' in request.session:
        del request.session['admin_id']
        del request.session['admin_role']
        del request.session['admin_name']
    return redirect('index_login')

@require_POST
def maintenance_add(request):
    tenant_id = request.session.get('tenant_id')
    if not tenant_id: return redirect('index_login')
    category = request.POST.get('category', '').strip()
    description = request.POST.get('description', '').strip()
    if not category or not description:
        messages.error(request, 'กรุณากรอกข้อมูลให้ครบถ้วน')
        return redirect('dashboard')
    try:
        tenant = Tenant.objects.get(id=tenant_id)
        active_contract = Contract.objects.filter(tenant=tenant, is_active=True).first()
        if not active_contract:
            messages.error(request, 'ไม่พบข้อมูลห้องพักของคุณ')
            return redirect('dashboard')
        full_description = f"[{category.upper()}] {description}"
        MaintenanceRequest.objects.create(room=active_contract.room, tenant=tenant, description=full_description, status='pending')
        messages.success(request, 'ส่งเรื่องแจ้งซ่อมเรียบร้อยแล้ว')
    except Exception as e:
        messages.error(request, f'เกิดข้อผิดพลาด: {str(e)}')
    return redirect('dashboard')


@require_POST
def payment_submit(request):
    tenant_id = request.session.get('tenant_id')
    if not tenant_id: return redirect('index_login')
    invoice_id = request.POST.get('invoice_id')
    slip_image = request.FILES.get('payment_slip')
    if not invoice_id or not slip_image:
        messages.error(request, 'กรุณาแนบไฟล์สลิปชำระเงิน')
        return redirect('dashboard')
    try:
        invoice = Invoice.objects.get(id=invoice_id, contract__tenant_id=tenant_id)
        invoice.is_paid = True
        invoice.save()
        messages.success(request, 'ส่งหลักฐานการชำระเงินเรียบร้อยแล้ว รอการตรวจสอบ')
    except Invoice.DoesNotExist:
        messages.error(request, 'ไม่พบข้อมูลใบแจ้งหนี้')
    return redirect('dashboard')

@require_POST
def tenant_add(request):
    if not request.session.get('admin_id'): return redirect('index_login')
    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    id_card_no = request.POST.get('id_card_no', '').strip()
    phone = request.POST.get('phone', '').strip()
    email = request.POST.get('email', '').strip()
    address = request.POST.get('address', '').strip()

    if not first_name or not last_name or not id_card_no or not phone:
        messages.error(request, 'กรุณากรอกข้อมูลสำคัญให้ครบถ้วน')
        return redirect('tenant')

    if Tenant.objects.filter(id_card_no=id_card_no).exists():
        messages.error(request, f'เลขบัตรประชาชน {id_card_no} มีอยู่ในระบบแล้ว')
        return redirect('tenant')

    Tenant.objects.create(first_name=first_name, last_name=last_name, id_card_no=id_card_no, phone=phone, email=email, address=address)
    messages.success(request, 'เพิ่มข้อมูลลูกบ้านเรียบร้อยแล้ว')
    return redirect('tenant')


@require_POST
def contract_add(request):
    if not request.session.get('admin_id'): return redirect('index_login')
    tenant_id = request.POST.get('tenant_id')
    room_id = request.POST.get('room_id')
    start_date = request.POST.get('start_date')
    deposit_raw = request.POST.get('deposit', '0')
    try:
        tenant = Tenant.objects.get(id=tenant_id)
        room = Room.objects.get(id=room_id)
        deposit = Decimal(deposit_raw)
        if room.status == 'occupied':
            messages.error(request, f'ห้อง {room.room_number} ไม่ว่าง')
            return redirect('main')
        Contract.objects.create(tenant=tenant, room=room, start_date=datetime.strptime(start_date, '%Y-%m-%d').date(), deposit=deposit, is_active=True)
        room.status = 'occupied'
        room.save()
        messages.success(request, f'ทำสัญญาเช่าห้อง {room.room_number} สำเร็จ')
    except Exception as e:
        messages.error(request, f'เกิดข้อผิดพลาด: {str(e)}')
    return redirect('main')

@require_POST
def invoice_add(request):
    if not request.session.get('admin_id'): return redirect('index_login')
    contract_id = request.POST.get('contract_id')
    due_date = request.POST.get('due_date')
    room_charge = Decimal(request.POST.get('room_charge', '0'))
    water_charge = Decimal(request.POST.get('water_charge', '0'))
    electricity_charge = Decimal(request.POST.get('electricity_charge', '0'))
    other_charge = Decimal(request.POST.get('other_charge', '0'))
    try:
        contract = Contract.objects.get(id=contract_id)
        total_amount = room_charge + water_charge + electricity_charge + other_charge
        Invoice.objects.create(contract=contract, due_date=datetime.strptime(due_date, '%Y-%m-%d').date(), room_charge=room_charge, water_charge=water_charge, electricity_charge=electricity_charge, other_charge=other_charge, total_amount=total_amount, is_paid=False)
        messages.success(request, f'ออกบิลค่าเช่าให้ห้อง {contract.room.room_number} เรียบร้อยแล้ว')
    except Exception as e:
        messages.error(request, f'เกิดข้อผิดพลาด: {str(e)}')
    return redirect('billing')

@require_POST
def config_update(request):
    if not request.session.get('admin_id'): return redirect('index_login')
    try:
        sys_info = SystemInfo.get_settings()
        sys_info.short_name = request.POST.get('short_name', '').strip()
        sys_info.full_name = request.POST.get('full_name', '').strip()
        sys_info.description = request.POST.get('description', '').strip()
        sys_info.address = request.POST.get('address', '').strip()
        sys_info.phone = request.POST.get('phone', '').strip()
        sys_info.email = request.POST.get('email', '').strip()
        sys_info.tax_id = request.POST.get('tax_id', '').strip()
        sys_info.water_rate = Decimal(request.POST.get('water_rate', '0.00'))
        sys_info.electricity_rate = Decimal(request.POST.get('electricity_rate', '0.00'))
        sys_info.promptpay_no = request.POST.get('promptpay_no', '').strip()
        sys_info.promptpay_name = request.POST.get('promptpay_name', '').strip()
        sys_info.save()
        messages.success(request, 'บันทึกข้อมูลการตั้งค่าอพาร์ทเมนต์สำเร็จ')
    except Exception as e:
        messages.error(request, f'เกิดข้อผิดพลาดในการบันทึกข้อมูล: {str(e)}')
    return redirect('config')

@require_POST
def admin_password_update(request):
    admin_id = request.session.get('admin_id')
    if not admin_id: return redirect('index_login')

    current_password = request.POST.get('current_password', '')
    new_password = request.POST.get('new_password', '')
    confirm_password = request.POST.get('confirm_password', '')

    if new_password != confirm_password:
        messages.error(request, 'การยืนยันรหัสผ่านใหม่ไม่ตรงกัน กรุณาลองใหม่อีกครั้ง')
        return redirect('config')

    if len(new_password) < 4:
        messages.error(request, 'รหัสผ่านต้องมีความยาวอย่างน้อย 4 ตัวอักษร')
        return redirect('config')

    try:
        admin = Admin.objects.get(id=admin_id)
        if not check_password(current_password, admin.password_hash):
            if not ('example_hash' in admin.password_hash and current_password == '1234'):
                messages.error(request, 'รหัสผ่านปัจจุบันไม่ถูกต้อง ไม่สามารถทำรายการได้')
                return redirect('config')
        admin.password_hash = make_password(new_password)
        admin.save()
        messages.success(request, 'เปลี่ยนรหัสผ่านสำหรับผู้ดูแลระบบเรียบร้อยแล้ว')
    except Admin.DoesNotExist:
        messages.error(request, 'ไม่พบข้อมูลผู้ดูแลระบบ')
    return redirect('config')

@require_POST
def room_type_add(request):
    if not request.session.get('admin_id'): return redirect('index_login')
    name = request.POST.get('name', '').strip()
    base_price_raw = request.POST.get('base_price', '').strip()
    description = request.POST.get('description', '').strip()

    if not name or not base_price_raw:
        messages.error(request, 'กรุณากรอกชื่อประเภทห้องและราคาเช่าพื้นฐาน')
        return redirect('main')

    try:
        base_price = Decimal(base_price_raw)
    except (InvalidOperation, ValueError):
        messages.error(request, 'ราคาเช่าพื้นฐานต้องเป็นตัวเลข')
        return redirect('main')

    RoomType.objects.create(name=name, base_price=base_price, description=description)
    messages.success(request, f'เพิ่มประเภทห้อง "{name}" เรียบร้อยแล้ว')
    return redirect('main')

def billing(request):
    admin_id = request.session.get('admin_id')
    if not admin_id: return redirect('index_login')
    
    admin = Admin.objects.get(id=admin_id)
    invoices_qs = Invoice.objects.select_related('contract__tenant', 'contract__room').prefetch_related('payments').all().order_by('-invoice_date', '-id')
    count_total = invoices_qs.count()
    count_unpaid = invoices_qs.filter(is_paid=False).count()
    count_paid = invoices_qs.filter(is_paid=True).count()
    paginator = Paginator(invoices_qs, 10)
    invoices = paginator.get_page(request.GET.get('page'))
    
    for inv in invoices:
        inv.latest_payment = inv.payments.all().last()

    active_contracts = Contract.objects.filter(is_active=True).select_related('room', 'tenant')

    return render(request, 'billing.html', {
        'admin': admin, 
        'invoices': invoices,
        'count_total': count_total,
        'count_unpaid': count_unpaid,
        'count_paid': count_paid,
        'active_contracts': active_contracts
    })

@require_POST
def invoice_edit(request, invoice_id):
    if not request.session.get('admin_id'): return redirect('index_login')
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        invoice.due_date = request.POST.get('due_date')
        invoice.room_charge = Decimal(request.POST.get('room_charge', '0'))
        invoice.water_charge = Decimal(request.POST.get('water_charge', '0'))
        invoice.electricity_charge = Decimal(request.POST.get('electricity_charge', '0'))
        invoice.other_charge = Decimal(request.POST.get('other_charge', '0'))
        invoice.total_amount = invoice.room_charge + invoice.water_charge + invoice.electricity_charge + invoice.other_charge
        invoice.is_paid = request.POST.get('is_paid') == 'True'
        invoice.save()
        messages.success(request, f'อัปเดตข้อมูลบิล INV-{invoice.id:04d} เรียบร้อยแล้ว')
    except Invoice.DoesNotExist:
        messages.error(request, 'ไม่พบบิลที่ต้องการแก้ไข')
    except Exception as e:
        messages.error(request, f'เกิดข้อผิดพลาด: {str(e)}')
    return redirect('billing')

@require_POST
def invoice_update_status(request, invoice_id):
    if not request.session.get('admin_id'): return redirect('index_login')
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        action_status = request.POST.get('status')
        latest_payment = Payment.objects.filter(invoice=invoice).last()
        
        if action_status == 'approve':
            invoice.is_paid = True
            if latest_payment:
                latest_payment.status = 'verified'
                latest_payment.save()
            messages.success(request, f'อนุมัติการชำระเงินสำหรับบิล INV-{invoice.id:04d} เรียบร้อยแล้ว')
        elif action_status == 'reject':
            invoice.is_paid = False
            if latest_payment:
                latest_payment.status = 'rejected'
                latest_payment.save()
            messages.warning(request, f'ปฏิเสธสลิปบิล INV-{invoice.id:04d} แล้ว (เก็บเป็นประวัติในระบบ)')
        invoice.save()
    except Exception as e:
        messages.error(request, f'เกิดข้อผิดพลาดในการเปลี่ยนสถานะ: {str(e)}')
    return redirect('billing')

@require_POST
def invoice_bulk_add(request):
    if not request.session.get('admin_id'): return redirect('index_login')
    try:
        invoice_date_str = request.POST.get('invoice_date')
        due_date_str = request.POST.get('due_date')
        invoice_date = datetime.strptime(invoice_date_str, '%Y-%m-%d').date()
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        selected_contracts = request.POST.getlist('selected_contracts')
        
        if not selected_contracts:
            messages.warning(request, 'ไม่ได้เลือกห้องสำหรับออกบิล')
            return redirect('billing')

        created_count = 0
        for contract_id in selected_contracts:
            try:
                contract = Contract.objects.get(id=contract_id, is_active=True)
                room_charge = Decimal(request.POST.get(f'room_charge_{contract.id}', '0.00'))
                water_charge = Decimal(request.POST.get(f'water_charge_{contract.id}', '0.00'))
                electricity_charge = Decimal(request.POST.get(f'electricity_charge_{contract.id}', '0.00'))
                other_charge = Decimal(request.POST.get(f'other_charge_{contract.id}', '0.00'))
                total_amount = room_charge + water_charge + electricity_charge + other_charge
                Invoice.objects.create(contract=contract, invoice_date=invoice_date, due_date=due_date, room_charge=room_charge, water_charge=water_charge, electricity_charge=electricity_charge, other_charge=other_charge, total_amount=total_amount, is_paid=False)
                created_count += 1
            except Exception as inner_e:
                print(f"Error creating invoice for contract {contract_id}: {inner_e}")
                
        messages.success(request, f'สร้างใบแจ้งหนี้เสร็จสิ้นจำนวน {created_count} รายการ')
    except Exception as e:
        messages.error(request, f'เกิดข้อผิดพลาด: {str(e)}')
    return redirect('billing')

@require_POST
def tenant_profile_update(request):
    tenant_id = request.session.get('tenant_id')
    if not tenant_id: return redirect('index_login')
    try:
        tenant = Tenant.objects.get(id=tenant_id)
        tenant.phone = request.POST.get('phone', '').strip()
        tenant.email = request.POST.get('email', '').strip()
        tenant.save()
        messages.success(request, 'อัปเดตข้อมูลติดต่อเรียบร้อยแล้ว')
    except Exception as e:
        messages.error(request, f'เกิดข้อผิดพลาด: {str(e)}')
    return redirect('dashboard')

@require_POST
def tenant_vehicle_add(request):
    tenant_id = request.session.get('tenant_id')
    if not tenant_id: return redirect('index_login')
    try:
        tenant = Tenant.objects.get(id=tenant_id)
        Vehicle.objects.create(
            tenant=tenant,
            vehicle_type=request.POST.get('vehicle_type', 'car'),
            license_plate=request.POST.get('license_plate', '').strip(),
            province=request.POST.get('province', '').strip(),
            brand=request.POST.get('brand', '').strip(),
            color=request.POST.get('color', '').strip(),
            note=request.POST.get('note', '').strip()
        )
        messages.success(request, 'เพิ่มข้อมูลรถสำเร็จ')
    except Exception as e:
        messages.error(request, 'เกิดข้อผิดพลาดในการเพิ่มรถ')
    return redirect('dashboard')

@require_POST
def tenant_vehicle_delete(request, vehicle_id):
    tenant_id = request.session.get('tenant_id')
    if not tenant_id: return redirect('index_login')
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id, tenant_id=tenant_id)
        vehicle.delete()
        messages.success(request, 'ลบข้อมูลรถเรียบร้อยแล้ว')
    except Vehicle.DoesNotExist:
        pass
    return redirect('dashboard')

@require_POST
def tenant_maintenance_add(request):
    tenant_id = request.session.get('tenant_id')
    if not tenant_id: return redirect('index_login')
    category = request.POST.get('category', '')
    description = request.POST.get('description', '').strip()
    try:
        tenant = Tenant.objects.get(id=tenant_id)
        active_contract = Contract.objects.filter(tenant=tenant, is_active=True).first()
        if not active_contract:
            messages.error(request, 'คุณยังไม่มีสัญญาเช่าที่ใช้งานอยู่ ไม่สามารถแจ้งซ่อมได้')
            return redirect('dashboard')
        full_desc = f"[{category}] {description}"
        MaintenanceRequest.objects.create(room=active_contract.room, tenant=tenant, description=full_desc, status='pending')
        messages.success(request, 'ส่งเรื่องแจ้งซ่อมเรียบร้อยแล้ว ช่างจะรีบดำเนินการให้เร็วที่สุด')
    except Exception as e:
        messages.error(request, 'เกิดข้อผิดพลาดในการแจ้งซ่อม')
    return redirect('dashboard')

@require_POST
def tenant_payment_submit(request):
    tenant_id = request.session.get('tenant_id')
    if not tenant_id: return redirect('index_login')
    invoice_id = request.POST.get('invoice_id')
    amount = request.POST.get('amount')
    slip_file = request.FILES.get('payment_slip')
    
    if not invoice_id or not slip_file:
        messages.error(request, 'กรุณาแนบไฟล์สลิปการโอนเงิน')
        return redirect('dashboard')
        
    try:
        invoice = Invoice.objects.get(id=invoice_id, contract__tenant_id=tenant_id)
        Payment.objects.create(invoice=invoice, amount=Decimal(amount), payment_method='bank_transfer', slip_image_url=slip_file, status='pending')
        messages.success(request, 'ส่งหลักฐานการชำระเงินเรียบร้อยแล้ว กรุณารอผู้ดูแลระบบตรวจสอบ')
    except Invoice.DoesNotExist:
        messages.error(request, 'ไม่พบข้อมูลใบแจ้งหนี้')
    except Exception as e:
        messages.error(request, f'เกิดข้อผิดพลาด: {str(e)}')
    return redirect('dashboard')

@require_POST
def tenant_settings_update(request):
    tenant_id = request.session.get('tenant_id')
    if not tenant_id: 
        return redirect('index_login')
    
    try:
        tenant = Tenant.objects.get(id=tenant_id)
        
        # รับค่าจาก Checkbox
        tenant.notify_email = request.POST.get('notify_email') == 'on'
        tenant.notify_line = request.POST.get('notify_line') == 'on'
        tenant.sync_calendar = request.POST.get('sync_calendar') == 'on'
        
        # อีเมลที่ใช้ซิงค์ปฏิทิน
        calendar_email = request.POST.get('calendar_email', '').strip()
        tenant.calendar_email = calendar_email if calendar_email else tenant.email
        
        tenant.save()
        messages.success(request, 'บันทึกการตั้งค่าระบบแจ้งเตือนและปฏิทินเรียบร้อยแล้ว')
        
    except Exception as e:
        messages.error(request, f'เกิดข้อผิดพลาดในการบันทึกการตั้งค่า: {str(e)}')
        
    return redirect('dashboard')

def contract(request):
    """รองรับการเข้าถึงหน้าสัญญาแบบไม่ได้ระบุ ID (หน้าเปล่า) ให้เข้าถึงได้สาธารณะเพื่อสร้างสัญญาใหม่"""
    
    if request.method == 'POST':
        # เอาส่วนนี้ออก เพื่อให้ไม่ต้องเป็น Admin ก็ Post ข้อมูลเข้ามาได้
        # if not request.session.get('admin_id'):
        #     return redirect('index_login')
            
        try:
            # 1. รับค่าที่กรอกเข้ามาจากฟอร์มหน้าสัญญา (อย่าลืมใส่ attribute name="..." ให้ครบในไฟล์ contract.html ด้วยนะครับ)
            tenant_name = request.POST.get('tenant_name', '').strip()
            id_card_no = request.POST.get('id_card_no', '').strip()
            tenant_address = request.POST.get('tenant_address', '').strip()
            tenant_phone = request.POST.get('tenant_phone', '').strip()
            room_number = request.POST.get('room_number')
            deposit_raw = request.POST.get('deposit', '0').replace(',', '')
            
            try:
                deposit = Decimal(deposit_raw) if deposit_raw else Decimal('0')
            except InvalidOperation:
                deposit = Decimal('0')

            # หากไม่ระบุห้องจะไม่สามารถสร้างสัญญาได้
            if not room_number:
                messages.error(request, 'กรุณาเลือกเลขห้องก่อนบันทึก')
                return redirect('contract')

            # 2. แยกชื่อนามสกุลผู้เช่า
            if not tenant_name:
                first_name = 'ไม่ระบุชื่อ'
                last_name = ''
            else:
                first_name, _, last_name = tenant_name.partition(' ')

            # 3. ตรวจสอบเลขบัตรประชาชนและเบอร์โทร (จำเป็นสำหรับการ Login ของลูกบ้าน)
            if not id_card_no:
                messages.error(request, 'กรุณากรอกเลขประจำตัวประชาชนของผู้เช่า (ใช้เป็นรหัสผ่านเข้าสู่ระบบ)')
                return redirect('contract')
                
            if not tenant_phone:
                messages.error(request, 'กรุณากรอกเบอร์โทรศัพท์ของผู้เช่า (ใช้เป็นรหัสผ่านเข้าสู่ระบบ)')
                return redirect('contract')

            # 4. บันทึกหรือค้นหาข้อมูลลูกบ้าน (Tenant) โดยใช้เลขบัตรประชาชนเป็นคีย์หลัก
            tenant, created = Tenant.objects.get_or_create(
                id_card_no=id_card_no,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone': tenant_phone,
                    'address': tenant_address
                }
            )

            # หากมีข้อมูลลูกบ้านจากเลขบัตรประชาชนนี้อยู่แล้วในระบบ ให้อัปเดตข้อมูลเป็นปัจจุบัน
            if not created:
                tenant.first_name = first_name
                tenant.last_name = last_name
                tenant.phone = tenant_phone
                tenant.address = tenant_address
                tenant.save()

            # 5. ค้นหาข้อมูลห้องที่ระบุมาว่าว่างจริงๆ หรือไม่
            room = Room.objects.get(room_number=room_number, status='available')

            # 6. บันทึกข้อมูลสัญญาลง Database
            new_contract = Contract.objects.create(
                tenant=tenant,
                room=room,
                start_date=datetime.now().date(),
                deposit=deposit,
                made_at=request.POST.get('made_at', ''),
                advance_payment_months=int(request.POST.get('advance_payment_months', 1)),
                rent_due_day=int(request.POST.get('rent_due_day', 5)),
                witness_1=request.POST.get('witness_1', ''),
                witness_2=request.POST.get('witness_2', ''),
                is_active=True
            )

            # 7. เปลี่ยนสถานะห้องพักเป็น "มีผู้เช่าแล้ว"
            room.status = 'occupied'
            room.save()

            # 8. ทำการ Auto-Login ให้ผู้เช่าเข้าสู่ระบบทันที
            request.session['tenant_id'] = tenant.id

            messages.success(request, f'สร้างสัญญาใหม่สำหรับห้อง {room.room_number} สำเร็จ กรุณาตรวจสอบความถูกต้องและลงนาม')
            # ทำการ Redirect เพื่อไปหน้ารายละเอียดของสัญญาที่เพิ่งสร้างเสร็จหมาดๆ
            return redirect('contract_detail', contract_id=new_contract.id)

        except Room.DoesNotExist:
            messages.error(request, 'ไม่พบห้องที่ระบุ หรือห้องนี้อาจจะถูกเช่าไปแล้ว')
        except Exception as e:
            messages.error(request, f'เกิดข้อผิดพลาดในการบันทึก: {str(e)}')
            
        return redirect('contract')

    # ---- สำหรับกรณี GET (เปิดหน้าเปล่าปกติเพื่อให้แอดมินพิมพ์ข้อมูล) ----
    available_rooms = Room.objects.filter(status='available').select_related('room_type').order_by('room_number')
    
    return render(request, 'contract.html', {
        'system_info': SystemInfo.get_settings(),
        'available_rooms': available_rooms
    })

@require_POST
def contract_save_details(request, contract_id):
    """ฟังก์ชันใหม่: รับค่าจากหน้ากระดาษที่แอดมินพิมพ์และบันทึกลงฐานข้อมูล"""
    if not request.session.get('admin_id'):
        return redirect('index_login')
    
    try:
        contract = Contract.objects.get(id=contract_id)
        
        # รับค่าและอัปเดต
        contract.made_at = request.POST.get('made_at', '')
        contract.advance_payment_months = int(request.POST.get('advance_payment_months', 1))
        contract.rent_due_day = int(request.POST.get('rent_due_day', 5))
        contract.witness_1 = request.POST.get('witness_1', '')
        contract.witness_2 = request.POST.get('witness_2', '')
        
        contract.save()
        messages.success(request, 'บันทึกข้อมูลรายละเอียดสัญญาเรียบร้อยแล้ว')
        
    except Contract.DoesNotExist:
        messages.error(request, 'ไม่พบสัญญาเช่า')
    except ValueError:
        messages.error(request, 'ข้อมูลตัวเลขที่กรอกไม่ถูกต้อง (ต้องเป็นตัวเลขเท่านั้น)')
        
    return redirect('contract_detail', contract_id=contract_id)

@require_POST
def tenant_contract_cancel(request):
    """ฟังก์ชันใหม่: สำหรับลูกบ้านกดยกเลิกสัญญาเช่าล่วงหน้า 30 วัน"""
    tenant_id = request.session.get('tenant_id')
    if not tenant_id: 
        return redirect('index_login')

    try:
        tenant = Tenant.objects.get(id=tenant_id)
        active_contract = Contract.objects.get(tenant=tenant, is_active=True)

        if not active_contract.is_cancel_requested:
            active_contract.is_cancel_requested = True
            # ตั้งวันที่มีผลคือ 30 วันนับจากวันนี้
            active_contract.cancel_effective_date = date.today() + timedelta(days=30)
            active_contract.save()
            messages.success(request, f'ส่งคำขอยกเลิกสัญญาเรียบร้อยแล้ว จะมีผลในวันที่ {active_contract.cancel_effective_date.strftime("%d/%m/%Y")}')
        else:
            messages.warning(request, 'คุณได้ทำการแจ้งยกเลิกสัญญาเช่าล่วงหน้าไปแล้ว')

    except Contract.DoesNotExist:
        messages.error(request, 'ไม่พบสัญญาเช่าที่กำลังใช้งานอยู่')
    except Exception as e:
        messages.error(request, f'เกิดข้อผิดพลาด: {str(e)}')

    return redirect('dashboard')