short name : ARM long name : Apartment Room Management command create django - MVT
1. django-admin startproject arm
2. cd arm
3. python manage.py startapp services
4. python manage.py runserver

if do not work do
1. 'py -m django startproject <name>'
2. cd <name>
3. 'py manage.py startapp services'
4. 'py manage.py runserver' how to setup go --> services --> view.py (create view)

install SQL 
1. pip install pymysql
2. python manage.py migrate <-- ใช้ติดตั้ง Table พื้นฐานสำหรับการใช้งาน

ระบบจัดการหอพัก (ARM - Apartment Room Management) 
├── 1. หน้าหลัก (Dashboard) 
│   ├── แสดงภาพรวม (Stats Cards) 
│   │   ├── จำนวนห้องทั้งหมด 
│   │   ├── จำนวนห้องว่าง 
│   │   ├── ยอดค้างชำระ 
│   │   └── รายการแจ้งซ่อมคงค้าง 
│   ├── ตารางสถานะห้องพักรายชั้น (Floor Status) 
│   ├── รายการแจ้งเตือนล่าสุด (Recent Alerts) 
│   └── ทางลัดการใช้งาน (Quick Actions) 
│ ├── 2. จัดการห้องพัก (Room Management) - [รองรับข้อ 7] 
│   ├── ผังห้องพักทั้งหมด (Floor Plan View) 
│   ├── ข้อมูลประเภทห้องและราคา (Room Types) 
│   └── สถานะการทำความสะอาด/ความพร้อมของห้อง 
│ ├── 3. จัดการผู้อาศัย (Tenant Management) - [รองรับข้อ 1] 
│   ├── ทะเบียนผู้เช่าปัจจุบัน (Active Tenants) 
│   ├── ระบบทำสัญญาเช่า/ต่อสัญญา (Contract Management) 
│   ├── ประวัติการย้ายเข้า-ย้ายออก (Tenant History) 
│   └── เอกสารแนบ (สำเนาบัตรประชาชน/ทะเบียนบ้าน) 
│ ├── 4. บัญชีและค่าเช่า (Billing & Accounting) - [รองรับข้อ 2, 5, 6] 
│   ├── บันทึกมิเตอร์น้ำ-ไฟ (Utility Meter Reading) 
│   ├── การออกใบแจ้งหนี้รายเดือน (Invoicing) 
│   ├── ระบบรับชำระเงินผ่านธนาคาร/แนบสลิป (Bank Payments) 
│   ├── ระบบตรวจสอบและยืนยันการชำระเงิน (Payment Verification) 
│   └── รายงานยอดค้างชำระ (Overdue Reports) 
│ ├── 5. ระบบแจ้งซ่อม (Maintenance System) - [รองรับข้อ 4] 
│   ├── รายการแจ้งซ่อมจากผู้เช่า (Maintenance Requests) 
│   ├── มอบหมายงานและติดตามสถานะ (Task Tracking) 
│   └── ประวัติการซ่อมบำรุงและค่าใช้จ่าย 
│ ├── 6. ประชาสัมพันธ์และการแจ้งเตือน (Announcements & Notifications) - [รองรับข้อ 3] 
│   ├── จัดการประกาศข่าวสาร (Public News) 
│   ├── ระบบส่งข้อความแจ้งเตือนผู้เช่าเมื่อถึงรอบบิล (Billing Alerts) 
│   └── แจ้งเตือนสถานะการแจ้งซ่อม (Maintenance Updates) 
│ └── 7. ตั้งค่าระบบ (System Settings) 
├── ข้อมูลหอพัก (Dormitory Profile) 
├── จัดการสิทธิ์ผู้ใช้งาน (User Roles/Admin) 
└── สำรองข้อมูลระบบ (Backup)

Mydatabase Schema (อัปเดตล่าสุดรองรับระบบชำระเงินและแจ้งเตือน)

-- 0. ตารางผู้ดูแลระบบ (Admin/Staff) - [เพิ่มใหม่สำหรับการแบ่งสิทธิ์]
CREATE TABLE admins (
id INT AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(50) NOT NULL UNIQUE COMMENT 'ชื่อผู้ใช้งาน (เข้าสู่ระบบหลังบ้าน)',
password_hash VARCHAR(255) NOT NULL COMMENT 'รหัสผ่านที่เข้ารหัสแล้ว',
first_name VARCHAR(100) NOT NULL COMMENT 'ชื่อจริง',
last_name VARCHAR(100) NOT NULL COMMENT 'นามสกุล',
role ENUM('owner', 'staff') DEFAULT 'staff' COMMENT 'ระดับสิทธิ์ (เจ้าของหอ, พนักงาน)',
is_active BOOLEAN DEFAULT TRUE COMMENT 'สถานะการใช้งาน'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 1. ตารางประเภทห้องพัก (RoomType)
CREATE TABLE room_types (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100) NOT NULL COMMENT 'ชื่อประเภทห้อง',
base_price DECIMAL(10, 2) NOT NULL COMMENT 'ราคาเช่าพื้นฐาน',
description TEXT COMMENT 'รายละเอียด'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. ตารางข้อมูลห้องพัก (Room)
CREATE TABLE rooms (
id INT AUTO_INCREMENT PRIMARY KEY,
room_number VARCHAR(10) NOT NULL UNIQUE COMMENT 'เลขห้อง',
floor INT NOT NULL COMMENT 'ชั้น',
room_type_id INT NOT NULL COMMENT 'รหัสประเภทห้อง',
status ENUM('available', 'occupied', 'maintenance') DEFAULT 'available' COMMENT 'สถานะ',
FOREIGN KEY (room_type_id) REFERENCES room_types(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. ตารางข้อมูลผู้เช่า (Tenant) - [สำหรับผู้ใช้งานทั่วไป Login]
CREATE TABLE tenants (
id INT AUTO_INCREMENT PRIMARY KEY,
first_name VARCHAR(100) NOT NULL COMMENT 'ชื่อ',
last_name VARCHAR(100) NOT NULL COMMENT 'นามสกุล',
phone VARCHAR(15) NOT NULL COMMENT 'เบอร์โทรศัพท์ (ใช้เสมือนรหัสผ่านหน้าเว็บ)',
id_card_no VARCHAR(13) NOT NULL UNIQUE COMMENT 'เลขบัตรประชาชน (ใช้เป็น Username หน้าเว็บ)',
email VARCHAR(254) DEFAULT NULL COMMENT 'อีเมล',
address TEXT NOT NULL COMMENT 'ที่อยู่ตามทะเบียนบ้าน'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. ตารางสัญญาเช่า (Contract)
CREATE TABLE contracts (
id INT AUTO_INCREMENT PRIMARY KEY,
tenant_id INT NOT NULL COMMENT 'รหัสผู้เช่า',
room_id INT NOT NULL COMMENT 'รหัสห้องพัก',
start_date DATE NOT NULL COMMENT 'วันที่เริ่มสัญญา',
end_date DATE DEFAULT NULL COMMENT 'วันที่สิ้นสุดสัญญา',
deposit DECIMAL(10, 2) NOT NULL COMMENT 'เงินประกัน',
is_active BOOLEAN DEFAULT TRUE COMMENT 'สถานะสัญญา (1=Active, 0=Inactive)',
FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. ตารางจดมิเตอร์น้ำ-ไฟ (UtilityRecord)
CREATE TABLE utility_records (
id INT AUTO_INCREMENT PRIMARY KEY,
room_id INT NOT NULL COMMENT 'รหัสห้องพัก',
recorded_date DATE DEFAULT (CURRENT_DATE) COMMENT 'วันที่จดบันทึก',
month INT NOT NULL COMMENT 'เดือน',
year INT NOT NULL COMMENT 'ปี',
water_meter FLOAT NOT NULL COMMENT 'เลขมิเตอร์น้ำ',
electricity_meter FLOAT NOT NULL COMMENT 'เลขมิเตอร์ไฟ',
FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. ตารางใบแจ้งหนี้ (Invoice)
CREATE TABLE invoices (
id INT AUTO_INCREMENT PRIMARY KEY,
contract_id INT NOT NULL COMMENT 'รหัสสัญญาเช่า',
invoice_date DATE DEFAULT (CURRENT_DATE) COMMENT 'วันที่ออกใบแจ้งหนี้',
due_date DATE NOT NULL COMMENT 'วันครบกำหนดชำระ',
room_charge DECIMAL(10, 2) NOT NULL COMMENT 'ค่าห้อง',
water_charge DECIMAL(10, 2) NOT NULL COMMENT 'ค่าน้ำ',
electricity_charge DECIMAL(10, 2) NOT NULL COMMENT 'ค่าไฟ',
other_charge DECIMAL(10, 2) DEFAULT 0.00 COMMENT 'ค่าใช้จ่ายอื่นๆ',
total_amount DECIMAL(10, 2) NOT NULL COMMENT 'ยอดรวมทั้งสิ้น',
is_paid BOOLEAN DEFAULT FALSE COMMENT 'สถานะการชำระเงิน (1=Paid, 0=Unpaid)',
FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. ตารางการรับชำระเงินและแนบสลิป (Payment)
CREATE TABLE payments (
id INT AUTO_INCREMENT PRIMARY KEY,
invoice_id INT NOT NULL COMMENT 'รหัสใบแจ้งหนี้',
payment_date DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'วันเวลาที่ชำระเงิน',
amount DECIMAL(10, 2) NOT NULL COMMENT 'จำนวนเงินที่โอน',
payment_method ENUM('bank_transfer', 'cash') DEFAULT 'bank_transfer' COMMENT 'ช่องทางการชำระเงิน',
slip_image_url VARCHAR(255) DEFAULT NULL COMMENT 'พาร์ทรูปภาพสลิปที่แนบ',
status ENUM('pending', 'verified', 'rejected') DEFAULT 'pending' COMMENT 'สถานะการตรวจสอบ (รอยืนยัน, ยืนยันแล้ว, ปฏิเสธ)',
note TEXT DEFAULT NULL COMMENT 'หมายเหตุเพิ่มเติมจากแอดมิน',
FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. ตารางการแจ้งซ่อม (MaintenanceRequest)
CREATE TABLE maintenance_requests (
id INT AUTO_INCREMENT PRIMARY KEY,
room_id INT NOT NULL COMMENT 'รหัสห้องพักที่แจ้งซ่อม',
tenant_id INT DEFAULT NULL COMMENT 'รหัสผู้เช่าที่แจ้ง (ถ้ามี)',
description TEXT NOT NULL COMMENT 'รายละเอียดปัญหา',
status ENUM('pending', 'in_progress', 'completed') DEFAULT 'pending' COMMENT 'สถานะการซ่อม',
created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'วันเวลาที่แจ้ง',
repair_cost DECIMAL(10, 2) DEFAULT 0.00 COMMENT 'ค่าซ่อมบำรุง',
FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE,
FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. ตารางการแจ้งเตือน (Notification)
CREATE TABLE notifications (
id INT AUTO_INCREMENT PRIMARY KEY,
tenant_id INT NOT NULL COMMENT 'รหัสผู้เช่าที่รับการแจ้งเตือน',
title VARCHAR(200) NOT NULL COMMENT 'หัวข้อการแจ้งเตือน',
message TEXT NOT NULL COMMENT 'ข้อความ',
is_read BOOLEAN DEFAULT FALSE COMMENT 'สถานะการอ่าน (1=อ่านแล้ว, 0=ยังไม่อ่าน)',
created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'วันเวลาที่ส่ง',
FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

Mock Data (ข้อมูลทดสอบระบบ)

-- ข้อมูลผู้ดูแลระบบ (Admin)
INSERT INTO admins (username, password_hash, first_name, last_name, role) VALUES
('admin', 'pbkdf2_sha256$260000$example_hash_for_admin', 'เจ้าของ', 'หอพัก', 'owner'),
('staff01', 'pbkdf2_sha256$260000$example_hash_for_staff', 'พนักงาน', 'ต้อนรับ', 'staff');

-- ข้อมูลประเภทห้อง
INSERT INTO room_types (name, base_price, description) VALUES
('พัดลม (Standard)', 3500.00, 'ห้องพัดลม เตียง 5 ฟุต ตู้เสื้อผ้า โต๊ะเครื่องแป้ง'),
('แอร์ (VIP)', 4500.00, 'ห้องแอร์ เครื่องทำน้ำอุ่น เตียง 5 ฟุต ตู้เสื้อผ้า โต๊ะทำงาน');

-- ข้อมูลห้องพัก
INSERT INTO rooms (room_number, floor, room_type_id, status) VALUES
('101', 1, 1, 'occupied'),
('102', 1, 1, 'available'),
('201', 2, 2, 'occupied'),
('202', 2, 2, 'maintenance');

-- ข้อมูลผู้เช่า
INSERT INTO tenants (first_name, last_name, phone, id_card_no, email, address) VALUES
('สมชาย', 'ใจดี', '0812345678', '1101234567890', 'somchai@email.com', '123 ม.1 ต.บางรัก อ.เมือง จ.กรุงเทพฯ'),
('สมศรี', 'มีทรัพย์', '0898765432', '2209876543210', 'somsri@email.com', '456 ม.2 ต.ช้างเผือก อ.เมือง จ.เชียงใหม่');

-- ข้อมูลสัญญาเช่า
INSERT INTO contracts (tenant_id, room_id, start_date, end_date, deposit, is_active) VALUES
(1, 1, '2023-01-01', '2023-12-31', 3500.00, 1),
(2, 3, '2023-05-01', '2024-04-30', 4500.00, 1);

-- ข้อมูลจดมิเตอร์น้ำ-ไฟ
INSERT INTO utility_records (room_id, recorded_date, month, year, water_meter, electricity_meter) VALUES
(1, '2023-10-25', 10, 2023, 125.5, 3450.0),
(3, '2023-10-25', 10, 2023, 80.0, 2100.5);

-- ข้อมูลใบแจ้งหนี้ (บิลค่าเช่า)
INSERT INTO invoices (contract_id, invoice_date, due_date, room_charge, water_charge, electricity_charge, other_charge, total_amount, is_paid) VALUES
(1, '2023-10-25', '2023-11-05', 3500.00, 150.00, 850.00, 0.00, 4500.00, 1),
(2, '2023-10-25', '2023-11-05', 4500.00, 120.00, 1200.00, 0.00, 5820.00, 0);

-- ข้อมูลการรับชำระเงิน (การแนบสลิป)
INSERT INTO payments (invoice_id, payment_date, amount, payment_method, slip_image_url, status) VALUES
(1, '2023-11-01 10:30:00', 4500.00, 'bank_transfer', '/media/slips/slip_1_20231101.jpg', 'verified');
INSERT INTO payments (invoice_id, payment_date, amount, payment_method, slip_image_url, status) VALUES
(2, '2023-11-04 15:45:00', 5820.00, 'bank_transfer', '/media/slips/slip_2_20231104.jpg', 'pending');

-- ข้อมูลการแจ้งซ่อม
INSERT INTO maintenance_requests (room_id, tenant_id, description, status, created_at, repair_cost) VALUES
(3, 2, 'แอร์ไม่เย็น มีน้ำหยด', 'in_progress', '2023-10-15 09:00:00', 0.00),
(4, NULL, 'หลอดไฟในห้องน้ำขาด (ห้องว่าง)', 'pending', '2023-10-20 14:00:00', 0.00);

-- ข้อมูลการแจ้งเตือน
INSERT INTO notifications (tenant_id, title, message, is_read, created_at) VALUES
(1, 'ยืนยันการชำระเงินเรียบร้อย', 'แอดมินได้ทำการยืนยันยอดชำระเงิน 4,500 บาท ของห้อง 101 ประจำเดือน 10/2023 แล้ว ขอบคุณครับ', 0, '2023-11-01 11:00:00'),
(2, 'แจ้งเตือนรอบบิลค่าเช่า', 'กรุณาชำระค่าเช่าห้อง 201 ประจำเดือน 10/2023 ยอดรวม 5,820 บาท ภายในวันที่ 05/11/2023', 1, '2023-10-26 08:00:00');

สร้าง password hash โดยใช้งานคำสั่งผ่าน CMD
python manage.py shell -c "from django.contrib.auth.hashers import make_password; print(f\"UPDATE admins SET password_hash = '{make_password('1234')}';\")"