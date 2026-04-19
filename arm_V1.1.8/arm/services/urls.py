from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # หน้า Login
    path('', views.index_login, name='index_login'),

    path('contract/', views.contract, name='contract'),

    # tenant role
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/tenant/', views.tenant_logout, name='tenant_logout'),

    # admin role
    path('main/', views.main, name='main'),
    path('tenant/', views.tenant, name='tenant'),
    path('billing/', views.billing, name='billing'),
    path('maintenance/', views.maintenance, name='maintenance'),
    path('config/', views.config, name='config'),
    path('logout/admin/', views.admin_logout, name='admin_logout'),

    # room CRUD
    path('room/add/', views.room_add, name='room_add'),
    path('room/<int:room_id>/edit/', views.room_edit, name='room_edit'),
    path('room/<int:room_id>/delete/', views.room_delete, name='room_delete'),

    # contract & maintenance actions
    path('contract/<int:contract_id>/', views.contract_detail, name='contract_detail'),
    path('contract/<int:contract_id>/sign/', views.contract_sign, name='contract_sign'),
    path('contract/<int:contract_id>/edit/', views.contract_edit, name='contract_edit'),
    
    # === เส้นทางใหม่: สำหรับแอดมินพิมพ์แก้ไขสัญญา ===
    path('contract/<int:contract_id>/save_details/', views.contract_save_details, name='contract_save_details'),
    
    path('maintenance/<int:request_id>/update/', views.maintenance_update, name='maintenance_update'),

    # === Tenant (ลูกบ้าน) ===
    path('maintenance/add/', views.maintenance_add, name='maintenance_add'),
    path('payment/submit/', views.payment_submit, name='payment_submit'),

    # === Admin (ผู้ดูแลระบบ) ===
    path('room-type/add/', views.room_type_add, name='room_type_add'),
    path('tenant/add/', views.tenant_add, name='tenant_add'),
    path('contract/add/', views.contract_add, name='contract_add'),
    path('invoice/add/', views.invoice_add, name='invoice_add'),
    path('config/update/', views.config_update, name='config_update'),
    path('config/password/update/', views.admin_password_update, name='admin_password_update'),

    # tenant CRUD
    path('tenant/<int:tenant_id>/edit/', views.tenant_edit, name='tenant_edit'),
    path('tenant/profile/update/', views.tenant_profile_update, name='tenant_profile_update'),
    path('tenant/settings/update/', views.tenant_settings_update, name='tenant_settings_update'),
    path('tenant/vehicle/add/', views.tenant_vehicle_add, name='tenant_vehicle_add'),
    path('tenant/vehicle/<int:vehicle_id>/delete/', views.tenant_vehicle_delete, name='tenant_vehicle_delete'),
    path('tenant/payment/submit/', views.tenant_payment_submit, name='tenant_payment_submit'),
    path('tenant/maintenance/add/', views.tenant_maintenance_add, name='tenant_maintenance_add'),
    
    # === เส้นทางใหม่: ลูกบ้านแจ้งยกเลิกสัญญาเช่า ===
    path('tenant/contract/cancel/', views.tenant_contract_cancel, name='tenant_contract_cancel'),
    
    # vehicle CRUD
    path('tenant/<int:tenant_id>/vehicle/add/', views.vehicle_add, name='vehicle_add'),
    path('vehicle/<int:vehicle_id>/delete/', views.vehicle_delete, name='vehicle_delete'),

    # invoice actions
    path('invoice/add/', views.invoice_add, name='invoice_add'),
    path('invoice/<int:invoice_id>/edit/', views.invoice_edit, name='invoice_edit'),
    path('invoice/<int:invoice_id>/update_status/', views.invoice_update_status, name='invoice_update_status'),
    path('invoice/bulk_add/', views.invoice_bulk_add, name='invoice_bulk_add'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)