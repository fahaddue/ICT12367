🏢 ARM System (Apartment Management System)

1. แนะนำโปรแกรม (Introduction)

ARM System คือระบบบริหารจัดการอพาร์ทเมนต์และหอพักแบบครบวงจร พัฒนาด้วยเฟรมเวิร์ก Django (Python) ระบบถูกออกแบบมาให้ครอบคลุมการทำงานทั้งฝั่งผู้ดูแลระบบ (Admin/Owner) และฝั่งลูกบ้าน (Tenant) เพื่อช่วยลดขั้นตอนการทำงานและเพิ่มความสะดวกในการจัดการหอพัก

ฟีเจอร์หลัก (Key Features):

ระบบผู้เช่า (Tenant Portal):

เข้าสู่ระบบง่ายๆ ด้วยเลขบัตรประชาชนและเบอร์โทรศัพท์

เซ็นสัญญาเช่าออนไลน์ด้วยระบบ Digital Signature (วาดลายเซ็นหรือพิมพ์)

ดูบิลค่าเช่า สแกน QR Code พร้อมเพย์ และแนบสลิปโอนเงินได้ด้วยตนเอง

จัดการข้อมูลส่วนตัวและยานพาหนะ

แจ้งซ่อมออนไลน์และติดตามสถานะได้ทันที

ระบบผู้ดูแล (Admin Portal):

หน้า Dashboard สรุปข้อมูลภาพรวม (จำนวนห้องว่าง, ห้องที่มีผู้เช่า, บิลค้างชำระ)

บริหารจัดการห้องพักและประเภทห้อง (Room Management)

จัดการข้อมูลผู้เช่าและสัญญาเช่า (พิมพ์เอกสารสัญญาเช่าได้)

ระบบคิดเงินและออกบิลแบบกลุ่ม (Bulk Billing) โดยคำนวณค่าน้ำ-ค่าไฟอัตโนมัติตามมิเตอร์

ตรวจเช็คและอนุมัติสลิปการโอนเงิน

อัปเดตสถานะการแจ้งซ่อมและบันทึกค่าใช้จ่าย

2. วิธีการติดตั้ง (Installation)

ข้อกำหนดเบื้องต้น: เครื่องคอมพิวเตอร์ต้องติดตั้ง Python 3.x ไว้เรียบร้อยแล้ว

โคลนโปรเจกต์หรือแตกไฟล์ Source Code:
เปิด Terminal/Command Prompt แล้วเข้าไปยังโฟลเดอร์โปรเจกต์ ARM/

สร้างและเปิดใช้งาน Virtual Environment (แนะนำ):

python -m venv env
# สำหรับ Windows
env\Scripts\activate
# สำหรับ Mac/Linux
source env/bin/activate


ติดตั้ง Packages ที่จำเป็น:

pip install -r requirements.txt


ตั้งค่าฐานข้อมูล (Database):
โปรเจกต์นี้ใช้ SQLite เป็นค่าเริ่มต้น คุณสามารถใช้ไฟล์ฐานข้อมูลที่มีอยู่แล้ว (db.sqlite3) หรือใช้คำสั่งเพื่อรัน Migration ใหม่:

python manage.py makemigrations
python manage.py migrate


(หมายเหตุ: หากต้องการใช้ข้อมูลตัวอย่าง สามารถ Import ข้อมูลจากไฟล์ arm_db_v1-0-4.sql ได้)

รันเซิร์ฟเวอร์:

python manage.py runserver


ระบบจะทำงานที่: http://127.0.0.1:8000/

3. วิธีการใช้งาน (Usage)

การเข้าสู่ระบบ (Login):

เข้าไปที่ URL: http://127.0.0.1:8000/

หน้าจอเข้าสู่ระบบจะสามารถสลับโหมดได้ (ผู้เช่า / ผู้ดูแลระบบ)

สำหรับผู้เช่า: กรอก "รหัสบัตรประชาชน (13 หลัก)" และ "เบอร์โทรศัพท์"

สำหรับผู้ดูแลระบบ: คลิกที่ปุ่ม "เข้าสู่ระบบสำหรับผู้ดูแลระบบ" ด้านล่าง แล้วกรอก "Username" และ "Password"

การทำงานฝั่ง Admin (Workflow แนะนำ):

ตั้งค่าระบบ: ไปที่เมนู ตั้งค่าอพาร์ทเมนต์ เพื่อกำหนดอัตราค่าน้ำ ค่าไฟ และข้อมูลพร้อมเพย์

จัดการห้อง: ไปที่ จัดการห้องพัก เพื่อเพิ่ม "ประเภทห้อง" และ "เพิ่มห้องพัก" ใหม่

รับผู้เช่า: ไปที่ ข้อมูลลูกบ้าน เพื่อสร้างสัญญาเช่า (กำหนดห้องที่ว่าง, ข้อมูลผู้เช่า, เงินมัดจำ)

ออกบิล: เมื่อถึงสิ้นเดือน ไปที่ ใบแจ้งหนี้ -> เลือก ออกบิลหลายห้อง กรอกเลขมิเตอร์น้ำ-ไฟ ระบบจะคำนวณเงินและสร้างบิลทันที

ตรวจรับเงิน: เมื่อผู้เช่าแนบสลิป สถานะบิลจะเปลี่ยนเป็น "รอยืนยัน" Admin สามารถกดยืนยันหรือปฏิเสธสลิปได้

4. User / Admin Password for Test (ข้อมูลสำหรับทดสอบ)

(หมายเหตุ: ข้อมูลด้านล่างเป็นข้อมูลจำลองสำหรับการทดสอบ หากไม่สามารถล็อกอินได้ ให้รันคำสั่ง python manage.py createsuperuser เพื่อสร้างแอดมินใหม่)

🧑‍💼 ผู้ดูแลระบบ (Admin Portal):

Username: admin

Password: 12345
(หรือใช้ account เจ้าของ: owner / owner1234 หากมี)

👤 ผู้เช่า (Tenant Portal):

เลขบัตรประชาชน (ID Card): 1111111111111 (พิมพ์เลข 1 จำนวน 13 ตัว)

เบอร์โทรศัพท์ (Phone): 1111111111
(หรือสามารถสร้างผู้เช่าคนใหม่จากฝั่งแอดมิน แล้วใช้ข้อมูลบัตรประชาชนและเบอร์โทรศัพท์ที่ตั้งไว้มาล็อกอินได้เลย)

5. โครงสร้างไฟล์ (Directory Structure)

ARM/
│
├── arm/                       # โฟลเดอร์การตั้งค่าหลักของ Django Project
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py            # ไฟล์กำหนดค่าโปรเจกต์ (Database, Apps, Static files)
│   ├── urls.py                # Routing หลักของระบบ
│   └── wsgi.py
│
├── media/                     # โฟลเดอร์เก็บไฟล์ที่ผู้ใช้อัปโหลด (สลิปโอนเงิน, ลายเซ็น)
│
├── services/                  # Django App หลักสำหรับตรรกะระบบหอพัก
│   ├── __pycache__/
│   ├── migrations/            # โฟลเดอร์จัดการเวอร์ชันของฐานข้อมูล
│   ├── static/                # เก็บไฟล์ CSS, JS, Images แบบคงที่
│   ├── templates/             # เก็บไฟล์ HTML (.html) ทั้งหมด (Base, Dashboard, Billing ฯลฯ)
│   ├── __init__.py
│   ├── admin.py               # ตั้งค่าการแสดงผลในหน้า Django Admin
│   ├── apps.py
│   ├── models.py              # โครงสร้างฐานข้อมูล (Room, Tenant, Invoice, Maintenance)
│   ├── tests.py
│   ├── urls.py                # Routing เฉพาะของ App Services
│   └── views.py               # ควบคุมการทำงานของแต่ละหน้าจอ (Logic & Controllers)
│
├── .env.example               # ตัวอย่างไฟล์เก็บ Environment variables
├── .gitignore                 # ไฟล์ละเว้นการอัปโหลดขึ้น Git
├── arm_db_v1-0-1.sql          # ไฟล์สำรองฐานข้อมูล SQL (เวอร์ชัน 1.0.1)
├── arm_db_v1-0-3.sql          # ไฟล์สำรองฐานข้อมูล SQL (เวอร์ชัน 1.0.3)
├── arm_db_v1-0-4.sql          # ไฟล์สำรองฐานข้อมูล SQL (เวอร์ชัน 1.0.4)
├── db.sqlite3                 # ฐานข้อมูลหลักของโปรเจกต์ (SQLite)
├── manage.py                  # ไฟล์ Script หลักสำหรับคำสั่งจัดการ Django
├── readme-.md                 # ไฟล์คู่มือแบบเก่า (ถ้ามี)
└── requirements.txt           # รายชื่อไลบรารี Python ที่โปรเจกต์ต้องใช้
6. Database Simple

-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.4.3 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping structure for table arm_live.admins
CREATE TABLE IF NOT EXISTS `admins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL COMMENT 'ชื่อผู้ใช้งาน (เข้าสู่ระบบหลังบ้าน)',
  `password_hash` varchar(255) NOT NULL COMMENT 'รหัสผ่านที่เข้ารหัสแล้ว',
  `first_name` varchar(100) NOT NULL COMMENT 'ชื่อจริง',
  `last_name` varchar(100) NOT NULL COMMENT 'นามสกุล',
  `role` enum('owner','staff') DEFAULT 'staff' COMMENT 'ระดับสิทธิ์ (เจ้าของหอ, พนักงาน)',
  `is_active` tinyint(1) DEFAULT '1' COMMENT 'สถานะการใช้งาน',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table arm_live.admins: ~1 rows (approximately)
INSERT INTO `admins` (`id`, `username`, `password_hash`, `first_name`, `last_name`, `role`, `is_active`) VALUES
	(1, 'admin', 'pbkdf2_sha256$1200000$7Xk9bweO7ddmsK3w8pEYvf$PoKJ9MdqVzwq2GDZ1g5cZbfWMIQVooBUVNQKFYgb/gU=', 'เจ้าของ', 'หอพัก', 'owner', 1);

-- Dumping structure for table arm_live.auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table arm_live.auth_group: ~0 rows (approximately)

-- Dumping structure for table arm_live.auth_group_permissions
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table arm_live.auth_group_permissions: ~0 rows (approximately)

-- Dumping structure for table arm_live.auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table arm_live.auth_permission: ~24 rows (approximately)
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 3, 'add_permission'),
	(6, 'Can change permission', 3, 'change_permission'),
	(7, 'Can delete permission', 3, 'delete_permission'),
	(8, 'Can view permission', 3, 'view_permission'),
	(9, 'Can add group', 2, 'add_group'),
	(10, 'Can change group', 2, 'change_group'),
	(11, 'Can delete group', 2, 'delete_group'),
	(12, 'Can view group', 2, 'view_group'),
	(13, 'Can add user', 4, 'add_user'),
	(14, 'Can change user', 4, 'change_user'),
	(15, 'Can delete user', 4, 'delete_user'),
	(16, 'Can view user', 4, 'view_user'),
	(17, 'Can add content type', 5, 'add_contenttype'),
	(18, 'Can change content type', 5, 'change_contenttype'),
	(19, 'Can delete content type', 5, 'delete_contenttype'),
	(20, 'Can view content type', 5, 'view_contenttype'),
	(21, 'Can add session', 6, 'add_session'),
	(22, 'Can change session', 6, 'change_session'),
	(23, 'Can delete session', 6, 'delete_session'),
	(24, 'Can view session', 6, 'view_session');

-- Dumping structure for table arm_live.auth_user
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table arm_live.auth_user: ~0 rows (approximately)

-- Dumping structure for table arm_live.auth_user_groups
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table arm_live.auth_user_groups: ~0 rows (approximately)

-- Dumping structure for table arm_live.auth_user_user_permissions
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table arm_live.auth_user_user_permissions: ~0 rows (approximately)

-- Dumping structure for table arm_live.contracts
CREATE TABLE IF NOT EXISTS `contracts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cancel_effective_date` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'ยกเลิกสัญญา',
  `tenant_id` int NOT NULL COMMENT 'รหัสผู้เช่า',
  `room_id` int NOT NULL COMMENT 'รหัสห้องพัก',
  `start_date` date NOT NULL COMMENT 'วันที่เริ่มสัญญา',
  `end_date` date DEFAULT NULL COMMENT 'วันที่สิ้นสุดสัญญา',
  `deposit` decimal(10,2) NOT NULL COMMENT 'เงินประกัน',
  `is_active` tinyint(1) DEFAULT '1' COMMENT 'สถานะสัญญา (1=Active, 0=Inactive)',
  `is_signed` tinyint(1) DEFAULT '0' COMMENT 'สถานะการเซ็นสัญญา',
  `signature_data` longtext COMMENT 'ข้อมูลลายเซ็น (Base64 หรือ ชื่อ)',
  `signature_type` varchar(20) DEFAULT NULL COMMENT 'ประเภทลายเซ็น (draw/type)',
  `signed_at` datetime DEFAULT NULL COMMENT 'วันเวลาที่เซ็นสัญญา',
  `made_at` varchar(255) DEFAULT NULL COMMENT 'สถานที่ทำสัญญา',
  `advance_payment_months` int DEFAULT '1' COMMENT 'ชำระล่วงหน้า (เดือน)',
  `rent_due_day` int DEFAULT '5' COMMENT 'กำหนดชำระภายในวันที่',
  `witness_1` varchar(150) DEFAULT NULL COMMENT 'ชื่อพยาน 1',
  `witness_2` varchar(150) DEFAULT NULL COMMENT 'ชื่อพยาน 2',
  `is_cancel_requested` int DEFAULT NULL COMMENT 'สถานะการเลิกเช่า',
  PRIMARY KEY (`id`),
  KEY `tenant_id` (`tenant_id`),
  KEY `room_id` (`room_id`),
  CONSTRAINT `contracts_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`) ON DELETE CASCADE,
  CONSTRAINT `contracts_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table arm_live.contracts: ~0 rows (approximately)

-- Dumping structure for table arm_live.django_admin_log
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_general_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table arm_live.django_admin_log: ~0 rows (approximately)

-- Dumping structure for table arm_live.django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table arm_live.django_content_type: ~6 rows (approximately)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(2, 'auth', 'group'),
	(3, 'auth', 'permission'),
	(4, 'auth', 'user'),
	(5, 'contenttypes', 'contenttype'),
	(6, 'sessions', 'session');

-- Dumping structure for table arm_live.django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table arm_live.django_migrations: ~18 rows (approximately)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2026-03-15 15:32:15.250613'),
	(2, 'auth', '0001_initial', '2026-03-15 15:32:15.874872'),
	(3, 'admin', '0001_initial', '2026-03-15 15:32:16.024725'),
	(4, 'admin', '0002_logentry_remove_auto_add', '2026-03-15 15:32:16.032987'),
	(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-03-15 15:32:16.040672'),
	(6, 'contenttypes', '0002_remove_content_type_name', '2026-03-15 15:32:16.125884'),
	(7, 'auth', '0002_alter_permission_name_max_length', '2026-03-15 15:32:16.191351'),
	(8, 'auth', '0003_alter_user_email_max_length', '2026-03-15 15:32:16.224068'),
	(9, 'auth', '0004_alter_user_username_opts', '2026-03-15 15:32:16.232685'),
	(10, 'auth', '0005_alter_user_last_login_null', '2026-03-15 15:32:16.288621'),
	(11, 'auth', '0006_require_contenttypes_0002', '2026-03-15 15:32:16.293048'),
	(12, 'auth', '0007_alter_validators_add_error_messages', '2026-03-15 15:32:16.306815'),
	(13, 'auth', '0008_alter_user_username_max_length', '2026-03-15 15:32:16.370881'),
	(14, 'auth', '0009_alter_user_last_name_max_length', '2026-03-15 15:32:16.436834'),
	(15, 'auth', '0010_alter_group_name_max_length', '2026-03-15 15:32:16.463743'),
	(16, 'auth', '0011_update_proxy_permissions', '2026-03-15 15:32:16.472642'),
	(17, 'auth', '0012_alter_user_first_name_max_length', '2026-03-15 15:32:16.536372'),
	(18, 'sessions', '0001_initial', '2026-03-15 15:32:16.571681');

-- Dumping structure for table arm_live.django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table arm_live.django_session: ~1 rows (approximately)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('q0b8macgdzvdhusexq782kx53igfb4uv', '.eJyrVkpMyc3Mi89MUbIy1IFyivJzUpWslPLL81KLlGCCeYm5IMGYUoNUEwMQaWABZluCSGMjsAiYNEoBs80VwJwkhJBhKlipIVjaUKkWANriJ3E:1wDy8r:EDJtAQ52zbCdB7YkaUHTlCfav_wEgmpkX7uZwe4Y_bY', '2026-05-02 05:22:53.993841');

-- Dumping structure for table arm_live.invoices
CREATE TABLE IF NOT EXISTS `invoices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `contract_id` int NOT NULL COMMENT 'รหัสสัญญาเช่า',
  `invoice_date` date DEFAULT (curdate()) COMMENT 'วันที่ออกใบแจ้งหนี้',
  `due_date` date NOT NULL COMMENT 'วันครบกำหนดชำระ',
  `room_charge` decimal(10,2) NOT NULL COMMENT 'ค่าห้อง',
  `water_charge` decimal(10,2) NOT NULL COMMENT 'ค่าน้ำ',
  `electricity_charge` decimal(10,2) NOT NULL COMMENT 'ค่าไฟ',
  `other_charge` decimal(10,2) DEFAULT '0.00' COMMENT 'ค่าใช้จ่ายอื่นๆ',
  `total_amount` decimal(10,2) NOT NULL COMMENT 'ยอดรวมทั้งสิ้น',
  `is_paid` tinyint(1) DEFAULT '0' COMMENT 'สถานะการชำระเงิน (1=Paid, 0=Unpaid)',
  PRIMARY KEY (`id`),
  KEY `contract_id` (`contract_id`),
  CONSTRAINT `invoices_ibfk_1` FOREIGN KEY (`contract_id`) REFERENCES `contracts` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table arm_live.invoices: ~0 rows (approximately)

-- Dumping structure for table arm_live.maintenance_requests
CREATE TABLE IF NOT EXISTS `maintenance_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room_id` int NOT NULL COMMENT 'รหัสห้องพักที่แจ้งซ่อม',
  `tenant_id` int DEFAULT NULL COMMENT 'รหัสผู้เช่าที่แจ้ง (ถ้ามี)',
  `description` text NOT NULL COMMENT 'รายละเอียดปัญหา',
  `status` enum('pending','in_progress','completed') DEFAULT 'pending' COMMENT 'สถานะการซ่อม',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'วันเวลาที่แจ้ง',
  `repair_cost` decimal(10,2) DEFAULT '0.00' COMMENT 'ค่าซ่อมบำรุง',
  `admin_remark` text,
  PRIMARY KEY (`id`),
  KEY `room_id` (`room_id`),
  KEY `tenant_id` (`tenant_id`),
  CONSTRAINT `maintenance_requests_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maintenance_requests_ibfk_2` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table arm_live.maintenance_requests: ~0 rows (approximately)

-- Dumping structure for table arm_live.notifications
CREATE TABLE IF NOT EXISTS `notifications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tenant_id` int NOT NULL COMMENT 'รหัสผู้เช่าที่รับการแจ้งเตือน',
  `title` varchar(200) NOT NULL COMMENT 'หัวข้อการแจ้งเตือน',
  `message` text NOT NULL COMMENT 'ข้อความ',
  `is_read` tinyint(1) DEFAULT '0' COMMENT 'สถานะการอ่าน (1=อ่านแล้ว, 0=ยังไม่อ่าน)',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'วันเวลาที่ส่ง',
  PRIMARY KEY (`id`),
  KEY `tenant_id` (`tenant_id`),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table arm_live.notifications: ~0 rows (approximately)

-- Dumping structure for table arm_live.payments
CREATE TABLE IF NOT EXISTS `payments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `invoice_id` int NOT NULL COMMENT 'รหัสใบแจ้งหนี้',
  `payment_date` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'วันเวลาที่ชำระเงิน',
  `amount` decimal(10,2) NOT NULL COMMENT 'จำนวนเงินที่โอน',
  `payment_method` enum('bank_transfer','cash') DEFAULT 'bank_transfer' COMMENT 'ช่องทางการชำระเงิน',
  `slip_image_url` varchar(255) DEFAULT NULL COMMENT 'พาร์ทรูปภาพสลิปที่แนบ',
  `status` enum('pending','wait','verified','confirm','rejected') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'สถานะการตรวจสอบ (รอยืนยัน, ยืนยันแล้ว, ปฏิเสธ)',
  `note` text COMMENT 'หมายเหตุเพิ่มเติมจากแอดมิน',
  PRIMARY KEY (`id`),
  KEY `invoice_id` (`invoice_id`),
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`invoice_id`) REFERENCES `invoices` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table arm_live.payments: ~0 rows (approximately)

-- Dumping structure for table arm_live.rooms
CREATE TABLE IF NOT EXISTS `rooms` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room_number` varchar(10) NOT NULL COMMENT 'เลขห้อง',
  `floor` int NOT NULL COMMENT 'ชั้น',
  `room_type_id` int NOT NULL COMMENT 'รหัสประเภทห้อง',
  `status` enum('available','occupied','maintenance') DEFAULT 'available' COMMENT 'สถานะ',
  PRIMARY KEY (`id`),
  UNIQUE KEY `room_number` (`room_number`),
  KEY `room_type_id` (`room_type_id`),
  CONSTRAINT `rooms_ibfk_1` FOREIGN KEY (`room_type_id`) REFERENCES `room_types` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table arm_live.rooms: ~0 rows (approximately)

-- Dumping structure for table arm_live.room_types
CREATE TABLE IF NOT EXISTS `room_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT 'ชื่อประเภทห้อง',
  `base_price` decimal(10,2) NOT NULL COMMENT 'ราคาเช่าพื้นฐาน',
  `description` text COMMENT 'รายละเอียด',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table arm_live.room_types: ~0 rows (approximately)

-- Dumping structure for table arm_live.system_info
CREATE TABLE IF NOT EXISTS `system_info` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'รหัสอ้างอิง (ปกติจะมีแค่ Record เดียวคือ id=1)',
  `short_name` varchar(200) NOT NULL COMMENT 'ขื่อย่อหอพัก / อพาร์ตเมนต์',
  `full_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'ชื่อเต็มหอพัก / อพาร์ตเมนต์',
  `description` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'รายละเอียดระบบ',
  `address` text COMMENT 'ที่อยู่หอพัก (สำหรับออกใบเสร็จ/ใบแจ้งหนี้)',
  `phone` varchar(50) DEFAULT NULL COMMENT 'เบอร์โทรศัพท์ติดต่อนิติบุคคล',
  `email` varchar(100) DEFAULT NULL COMMENT 'อีเมลติดต่อ',
  `tax_id` varchar(20) DEFAULT NULL COMMENT 'เลขประจำตัวผู้เสียภาษี (ถ้ามี)',
  `water_rate` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'ราคาค่าน้ำประปา (ต่อหน่วย)',
  `electricity_rate` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'ราคาค่าไฟฟ้า (ต่อหน่วย)',
  `promptpay_no` varchar(20) DEFAULT NULL COMMENT 'หมายเลขพร้อมเพย์ (สำหรับสร้าง QR Code ชำระเงิน)',
  `promptpay_name` varchar(100) DEFAULT NULL COMMENT 'ชื่อบัญชีพร้อมเพย์',
  `system_version` varchar(20) DEFAULT '1.0.0' COMMENT 'เวอร์ชันของระบบปัจจุบัน',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'วันเวลาที่อัปเดตข้อมูลล่าสุด',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='ตารางเก็บข้อมูลตั้งค่าพื้นฐานของระบบ';

-- Dumping data for table arm_live.system_info: ~1 rows (approximately)
INSERT INTO `system_info` (`id`, `short_name`, `full_name`, `description`, `address`, `phone`, `email`, `tax_id`, `water_rate`, `electricity_rate`, `promptpay_no`, `promptpay_name`, `system_version`, `updated_at`) VALUES
	(1, 'ARM', 'Apartment Room Management', 'ระบบจัดการห้องพัก', 'โชคกมล อพาร์ทเม้นท์ 73 ซอย จิ๊ปดำริห์ รัชดาภิเษก ดินแดง กรุงเทพฯ 10400', '0838625365', 'nontawat.work321@gmail.com', '0105578659843', 10.00, 4.00, '0936834288', 'Pussy', '1.0.2', '2026-04-17 14:59:04');

-- Dumping structure for table arm_live.tenants
CREATE TABLE IF NOT EXISTS `tenants` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL COMMENT 'ชื่อ',
  `last_name` varchar(100) NOT NULL COMMENT 'นามสกุล',
  `phone` varchar(15) NOT NULL COMMENT 'เบอร์โทรศัพท์',
  `gender` enum('female','male') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'เพศ',
  `id_card_no` varchar(13) NOT NULL COMMENT 'เลขบัตรประชาชน (ใช้เป็น Username Login)',
  `email` varchar(254) DEFAULT NULL COMMENT 'อีเมล',
  `address` text NOT NULL COMMENT 'ที่อยู่ตามทะเบียนบ้าน',
  `avatar` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'รูปภาพ',
  `notify_email` tinyint(1) DEFAULT '1',
  `notify_line` tinyint(1) DEFAULT '0',
  `sync_calendar` tinyint(1) DEFAULT '0',
  `calendar_email` varchar(254) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_card_no` (`id_card_no`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table arm_live.tenants: ~0 rows (approximately)

-- Dumping structure for table arm_live.vehicles
CREATE TABLE IF NOT EXISTS `vehicles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tenant_id` int NOT NULL COMMENT 'รหัสผู้เช่า (เชื่อมกับตาราง tenants)',
  `license_plate` varchar(20) NOT NULL COMMENT 'ป้ายทะเบียน (เช่น กค 1234)',
  `province` varchar(50) NOT NULL COMMENT 'จังหวัดของป้ายทะเบียน',
  `brand` varchar(50) DEFAULT NULL COMMENT 'ยี่ห้อรถ (เช่น Honda, Toyota)',
  `color` varchar(20) DEFAULT NULL COMMENT 'สีรถ',
  `vehicle_type` varchar(20) DEFAULT 'car' COMMENT 'ประเภทรถ (car, motorcycle, other)',
  `note` text COMMENT 'หมายเหตุเพิ่มเติม',
  `registered_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'วันที่บันทึกข้อมูลรถ',
  PRIMARY KEY (`id`),
  KEY `tenant_id` (`tenant_id`),
  CONSTRAINT `vehicles_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='ตารางเก็บข้อมูลยานพาหนะของผู้เช่า';

-- Dumping data for table arm_live.vehicles: ~0 rows (approximately)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
