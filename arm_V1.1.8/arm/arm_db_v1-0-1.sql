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

-- Dumping data for table arm_live.admins: ~2 rows (approximately)
INSERT INTO `admins` (`id`, `username`, `password_hash`, `first_name`, `last_name`, `role`, `is_active`) VALUES
	(1, 'admin', 'pbkdf2_sha256$260000$example_hash_for_admin', 'เจ้าของ', 'หอพัก', 'owner', 1),
	(2, 'staff01', 'pbkdf2_sha256$260000$example_hash_for_staff', 'พนักงาน', 'ต้อนรับ', 'staff', 1);

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
  `tenant_id` int NOT NULL COMMENT 'รหัสผู้เช่า',
  `room_id` int NOT NULL COMMENT 'รหัสห้องพัก',
  `start_date` date NOT NULL COMMENT 'วันที่เริ่มสัญญา',
  `end_date` date DEFAULT NULL COMMENT 'วันที่สิ้นสุดสัญญา',
  `deposit` decimal(10,2) NOT NULL COMMENT 'เงินประกัน',
  `is_active` tinyint(1) DEFAULT '1' COMMENT 'สถานะสัญญา (1=Active, 0=Inactive)',
  PRIMARY KEY (`id`),
  KEY `tenant_id` (`tenant_id`),
  KEY `room_id` (`room_id`),
  CONSTRAINT `contracts_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`) ON DELETE CASCADE,
  CONSTRAINT `contracts_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table arm_live.contracts: ~2 rows (approximately)
INSERT INTO `contracts` (`id`, `tenant_id`, `room_id`, `start_date`, `end_date`, `deposit`, `is_active`) VALUES
	(1, 1, 1, '2023-01-01', '2023-12-31', 3500.00, 1),
	(2, 2, 3, '2023-05-01', '2024-04-30', 4500.00, 1);

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

-- Dumping data for table arm_live.django_migrations: ~5 rows (approximately)
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

-- Dumping data for table arm_live.django_session: ~0 rows (approximately)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('346938o5anvjbp6woiseonk91utedzj0', 'eyJ0ZW5hbnRfaWQiOjF9:1w1o8N:hytRsl8sBaifKQYL9hjN_0kWag5RYcQbhzM99p7jGyc', '2026-03-29 16:16:07.094477');

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table arm_live.invoices: ~2 rows (approximately)
INSERT INTO `invoices` (`id`, `contract_id`, `invoice_date`, `due_date`, `room_charge`, `water_charge`, `electricity_charge`, `other_charge`, `total_amount`, `is_paid`) VALUES
	(1, 1, '2023-10-25', '2023-11-05', 3500.00, 150.00, 850.00, 0.00, 4500.00, 1),
	(2, 2, '2023-10-25', '2023-11-05', 4500.00, 120.00, 1200.00, 0.00, 5820.00, 0);

-- Dumping structure for table arm_live.maintenance_requests
CREATE TABLE IF NOT EXISTS `maintenance_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room_id` int NOT NULL COMMENT 'รหัสห้องพักที่แจ้งซ่อม',
  `tenant_id` int DEFAULT NULL COMMENT 'รหัสผู้เช่าที่แจ้ง (ถ้ามี)',
  `description` text NOT NULL COMMENT 'รายละเอียดปัญหา',
  `status` enum('pending','in_progress','completed') DEFAULT 'pending' COMMENT 'สถานะการซ่อม',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'วันเวลาที่แจ้ง',
  `repair_cost` decimal(10,2) DEFAULT '0.00' COMMENT 'ค่าซ่อมบำรุง',
  PRIMARY KEY (`id`),
  KEY `room_id` (`room_id`),
  KEY `tenant_id` (`tenant_id`),
  CONSTRAINT `maintenance_requests_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`) ON DELETE CASCADE,
  CONSTRAINT `maintenance_requests_ibfk_2` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table arm_live.maintenance_requests: ~2 rows (approximately)
INSERT INTO `maintenance_requests` (`id`, `room_id`, `tenant_id`, `description`, `status`, `created_at`, `repair_cost`) VALUES
	(1, 3, 2, 'แอร์ไม่เย็น มีน้ำหยด', 'in_progress', '2023-10-15 09:00:00', 0.00),
	(2, 4, NULL, 'หลอดไฟในห้องน้ำขาด (ห้องว่าง)', 'pending', '2023-10-20 14:00:00', 0.00);

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

-- Dumping data for table arm_live.notifications: ~2 rows (approximately)
INSERT INTO `notifications` (`id`, `tenant_id`, `title`, `message`, `is_read`, `created_at`) VALUES
	(1, 1, 'ยืนยันการชำระเงินเรียบร้อย', 'แอดมินได้ทำการยืนยันยอดชำระเงิน 4,500 บาท ของห้อง 101 ประจำเดือน 10/2023 แล้ว ขอบคุณครับ', 0, '2023-11-01 11:00:00'),
	(2, 2, 'แจ้งเตือนรอบบิลค่าเช่า', 'กรุณาชำระค่าเช่าห้อง 201 ประจำเดือน 10/2023 ยอดรวม 5,820 บาท ภายในวันที่ 05/11/2023', 1, '2023-10-26 08:00:00');

-- Dumping structure for table arm_live.payments
CREATE TABLE IF NOT EXISTS `payments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `invoice_id` int NOT NULL COMMENT 'รหัสใบแจ้งหนี้',
  `payment_date` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'วันเวลาที่ชำระเงิน',
  `amount` decimal(10,2) NOT NULL COMMENT 'จำนวนเงินที่โอน',
  `payment_method` enum('bank_transfer','cash') DEFAULT 'bank_transfer' COMMENT 'ช่องทางการชำระเงิน',
  `slip_image_url` varchar(255) DEFAULT NULL COMMENT 'พาร์ทรูปภาพสลิปที่แนบ',
  `status` enum('pending','verified','rejected') DEFAULT 'pending' COMMENT 'สถานะการตรวจสอบ (รอยืนยัน, ยืนยันแล้ว, ปฏิเสธ)',
  `note` text COMMENT 'หมายเหตุเพิ่มเติมจากแอดมิน',
  PRIMARY KEY (`id`),
  KEY `invoice_id` (`invoice_id`),
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`invoice_id`) REFERENCES `invoices` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table arm_live.payments: ~2 rows (approximately)
INSERT INTO `payments` (`id`, `invoice_id`, `payment_date`, `amount`, `payment_method`, `slip_image_url`, `status`, `note`) VALUES
	(1, 1, '2023-11-01 10:30:00', 4500.00, 'bank_transfer', '/media/slips/slip_1_20231101.jpg', 'verified', NULL),
	(2, 2, '2023-11-04 15:45:00', 5820.00, 'bank_transfer', '/media/slips/slip_2_20231104.jpg', 'pending', NULL);

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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table arm_live.rooms: ~3 rows (approximately)
INSERT INTO `rooms` (`id`, `room_number`, `floor`, `room_type_id`, `status`) VALUES
	(1, '101', 1, 1, 'occupied'),
	(2, '102', 1, 1, 'available'),
	(3, '201', 2, 2, 'occupied'),
	(4, '202', 2, 2, 'maintenance');

-- Dumping structure for table arm_live.room_types
CREATE TABLE IF NOT EXISTS `room_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT 'ชื่อประเภทห้อง',
  `base_price` decimal(10,2) NOT NULL COMMENT 'ราคาเช่าพื้นฐาน',
  `description` text COMMENT 'รายละเอียด',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table arm_live.room_types: ~2 rows (approximately)
INSERT INTO `room_types` (`id`, `name`, `base_price`, `description`) VALUES
	(1, 'พัดลม (Standard)', 3500.00, 'ห้องพัดลม เตียง 5 ฟุต ตู้เสื้อผ้า โต๊ะเครื่องแป้ง'),
	(2, 'แอร์ (VIP)', 4500.00, 'ห้องแอร์ เครื่องทำน้ำอุ่น เตียง 5 ฟุต ตู้เสื้อผ้า โต๊ะทำงาน');

-- Dumping structure for table arm_live.tenants
CREATE TABLE IF NOT EXISTS `tenants` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL COMMENT 'ชื่อ',
  `last_name` varchar(100) NOT NULL COMMENT 'นามสกุล',
  `phone` varchar(15) NOT NULL COMMENT 'เบอร์โทรศัพท์',
  `id_card_no` varchar(13) NOT NULL COMMENT 'เลขบัตรประชาชน (ใช้เป็น Username Login)',
  `email` varchar(254) DEFAULT NULL COMMENT 'อีเมล',
  `address` text NOT NULL COMMENT 'ที่อยู่ตามทะเบียนบ้าน',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_card_no` (`id_card_no`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table arm_live.tenants: ~2 rows (approximately)
INSERT INTO `tenants` (`id`, `first_name`, `last_name`, `phone`, `id_card_no`, `email`, `address`) VALUES
	(1, 'สมชาย', 'ใจดี', '0812345678', '1101234567890', 'somchai@email.com', '123 ม.1 ต.บางรัก อ.เมือง จ.กรุงเทพฯ'),
	(2, 'สมศรี', 'มีทรัพย์', '0898765432', '2209876543210', 'somsri@email.com', '456 ม.2 ต.ช้างเผือก อ.เมือง จ.เชียงใหม่');

-- Dumping structure for table arm_live.utility_records
CREATE TABLE IF NOT EXISTS `utility_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room_id` int NOT NULL COMMENT 'รหัสห้องพัก',
  `recorded_date` date DEFAULT (curdate()) COMMENT 'วันที่จดบันทึก',
  `month` int NOT NULL COMMENT 'เดือน',
  `year` int NOT NULL COMMENT 'ปี',
  `water_meter` float NOT NULL COMMENT 'เลขมิเตอร์น้ำ',
  `electricity_meter` float NOT NULL COMMENT 'เลขมิเตอร์ไฟ',
  PRIMARY KEY (`id`),
  KEY `room_id` (`room_id`),
  CONSTRAINT `utility_records_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table arm_live.utility_records: ~2 rows (approximately)
INSERT INTO `utility_records` (`id`, `room_id`, `recorded_date`, `month`, `year`, `water_meter`, `electricity_meter`) VALUES
	(1, 1, '2023-10-25', 10, 2023, 125.5, 3450),
	(2, 3, '2023-10-25', 10, 2023, 80, 2100.5);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
