# Web Piket SILAB - Django Frontend

Web application untuk consume API Piket dengan fitur lengkap manajemen absensi piket menggunakan face recognition.

## 📋 Fitur

### 1. **Authentication & Profile**
- ✅ Register user baru
- ✅ Login/Logout
- ✅ Update profile (nama, NPM, password)

### 2. **Face Vector Management**
- ✅ Tambah vektor wajah dengan streaming kamera (20 foto otomatis)
- ✅ Tambah vektor wajah dengan upload foto
- ✅ Update vektor wajah (ganti dengan 20 foto baru)

### 3. **Manajemen Periode Piket**
- ✅ CRUD periode piket
- ✅ Pilih kepengurusan lab dari dropdown
- ✅ Aktifkan/nonaktifkan periode
- ✅ Set tanggal mulai & selesai

### 4. **Manajemen Jadwal Piket**
- ✅ CRUD jadwal piket
- ✅ Pilih kepengurusan lab dari dropdown
- ✅ Assign user ke hari tertentu
- ✅ List semua jadwal

### 5. **Absensi Piket**
- ✅ Mulai piket dengan face recognition
- ✅ Akhiri piket dengan face verification + input kegiatan
- ✅ Dashboard status piket hari ini

### 6. **Report Absensi**
- ✅ List semua absensi dengan filter (periode, user)
- ✅ Tampilkan: nomor, nama, NPM, jam masuk, jam keluar, durasi, kegiatan
- ✅ Export data (coming soon)

## 🛠️ Teknologi

- **Framework**: Django 5.1+
- **Database**: MySQL 8.0+ (SILAB)
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **API Integration**: Python Requests
- **Camera**: WebRTC getUserMedia API

## 📦 Instalasi

### 1. Setup Python Environment

```powershell
# Buat virtual environment
python -m venv venv

# Aktivasi virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Konfigurasi Database

```powershell
# Copy .env.example ke .env
copy .env.example .env

# Edit file .env
notepad .env
```

Isi `.env`:

```env
# Django Configuration
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=silab
DB_USER=root
DB_PASSWORD=your_mysql_password

# API Piket Configuration
API_PIKET_URL=http://localhost:5000
```

### 3. Pastikan Database SILAB Sudah Ada

Web ini menggunakan database SILAB yang sama dengan API Piket. Pastikan database sudah diimport dan API Piket sudah running.

```sql
-- Cek database
mysql -u root -p -e "USE silab; SHOW TABLES;"
```

### 4. Jalankan Aplikasi

```powershell
# Run Django development server
python manage.py runserver

# Atau dengan port custom
python manage.py runserver 8000
```

Web akan berjalan di: **`http://localhost:8000`**

## 📁 Struktur Project

```
web/
├── manage.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
│
├── web_piket/              # Django project
│   ├── __init__.py
│   ├── settings.py         # Konfigurasi Django
│   ├── urls.py             # URL routing utama
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/               # App: Authentication & Profile
│   ├── models.py           # Users, Profile models
│   ├── views.py            # register, login, profile views
│   └── urls.py
│
├── face_vectors/           # App: Face Vector Management
│   ├── views.py            # insert, update face vectors
│   └── urls.py
│
├── piket_management/       # App: CRUD Periode & Jadwal
│   ├── models.py           # PeriodePiket, JadwalPiket, KepengurusanLab models
│   ├── views.py            # CRUD views
│   └── urls.py
│
├── attendance/             # App: Absensi & Report
│   ├── models.py           # Absensi model
│   ├── views.py            # mulai, akhiri, report views
│   └── urls.py
│
└── templates/              # HTML Templates
    ├── base.html           # Base template + Bootstrap
    ├── accounts/           # Login, register, profile
    ├── face_vectors/       # Insert, update face vectors
    ├── piket_management/   # Periode & jadwal CRUD
    └── attendance/         # Dashboard, mulai, akhiri, report
```

## 🎯 Flow Penggunaan

### 1. Setup Awal (Admin)

```
1. Register user pertama
2. Login
3. Setup kepengurusan lab (Manajemen > Kepengurusan Lab)
4. Buat periode piket aktif (Manajemen > Periode Piket)
5. Buat jadwal piket untuk setiap user (Manajemen > Jadwal Piket)
```

### 2. Setup Vektor Wajah (User)

```
1. Login
2. Wajah > Tambah Vektor Wajah > Buka Kamera
3. Sistem capture 20 foto otomatis
4. Vektor disimpan ke API Piket
```

### 3. Absensi Piket Harian

```
1. Login di pagi hari
2. Dashboard > Mulai Piket
3. Ambil foto wajah (face recognition)
4. ...lakukan kegiatan piket...
5. Dashboard > Akhiri Piket
6. Ambil foto wajah + isi kegiatan
7. Selesai
```

### 4. Monitoring & Report

```
1. Dashboard > Report Absensi
2. Filter by periode atau user
3. Lihat detail kegiatan setiap absensi
```

## 🔌 Integrasi dengan API Piket

Web ini consume 6 endpoint dari API Piket:

### 1. Health Check
```python
GET http://localhost:5000/health
# Response: {"status": "ok", "message": "..."}
```

### 2. Insert Face Vectors (Camera)
```python
POST http://localhost:5000/api/face/insert
# Body: {"user_id": "...", "images": ["data:image/...", ...]}
```

### 3. Update Face Vectors
```python
PUT http://localhost:5000/api/face/update/<user_id>
# Body: {"images": ["data:image/...", ...]}
```

### 4. Insert Face Vector (Upload)
```python
POST http://localhost:5000/api/face/insert-from-photo
# Body: {"user_id": "...", "image": "data:image/..."}
```

### 5. Mulai Piket
```python
POST http://localhost:5000/api/piket/mulai
# Body: {"image": "data:image/..."}
```

### 6. Akhiri Piket
```python
POST http://localhost:5000/api/piket/akhiri
# Body: {"image": "data:image/...", "kegiatan": "..."}
```

## 🎨 UI/UX Features

### Bootstrap 5 Components
- Responsive navbar with dropdown
- Card-based layouts
- Form validation
- Modals for kegiatan detail
- Alert messages (success, error, warning)
- Progress bars for capture status

### Camera Streaming
- Auto-start camera on page load
- Real-time video preview
- Auto-capture 20 photos (500ms delay)
- Progress overlay during capture
- Error handling for camera access

### JavaScript Functions
```javascript
startCamera(videoElementId)       // Start webcam
stopCamera()                      // Stop webcam
captureImage(videoElementId)      // Capture single frame
captureMultipleImages(id, count, delay)  // Auto-capture multiple
```

## 🔒 Security Notes

- ✅ CSRF protection enabled
- ✅ Session-based authentication
- ✅ Password hashing (Django default)
- ⚠️ No HTTPS in development (use in production)
- ⚠️ No rate limiting (add in production)

## 🐛 Troubleshooting

### Problem 1: Database connection error

```powershell
# Cek koneksi MySQL
mysql -u root -p silab -e "SELECT 1"

# Cek settings di .env
```

### Problem 2: API Piket tidak tersambung

```
Error: Connection refused to http://localhost:5000

Solusi:
1. Pastikan API Piket sudah running (python app.py)
2. Cek API_PIKET_URL di .env
3. Test dengan: curl http://localhost:5000/health
```

### Problem 3: Camera tidak bisa diakses

```
Error: NotAllowedError atau NotFoundError

Solusi:
1. Allow camera permission di browser
2. Gunakan HTTPS (atau localhost)
3. Cek apakah kamera sedang digunakan aplikasi lain
```

### Problem 4: Foreign key constraint error

```
Error: Cannot add or update a child row: a foreign key constraint fails 
(`silab`.`periode_piket`, CONSTRAINT `periode_piket_kepengurusan_lab_id_foreign`)

Penyebab: 
Mencoba create periode/jadwal tanpa memilih kepengurusan lab yang valid.

Solusi:
1. Pastikan ada data kepengurusan_lab di database
2. Pilih kepengurusan lab dari dropdown (WAJIB)
3. Jangan biarkan field kepengurusan_lab_id kosong
```

### Problem 5: Unknown column 'absensi.user_id'

```
Error: Unknown column 'absensi.user_id' in 'field list'

Penyebab:
Web Django dan API sudah diupdate tapi ada cached models lama.

Solusi:
1. Restart Django server: Ctrl+C lalu python manage.py runserver
2. Restart API Piket server
3. Clear browser cache (Ctrl+Shift+Del)
4. Hapus folder __pycache__ di semua apps
```

### Problem 6: Face not recognized

```
Error: Face not recognized. Please register first.

Solusi:
1. Pastikan sudah tambah vektor wajah (min 15-20 foto)
2. Pencahayaan harus cukup
3. Wajah menghadap kamera frontal
4. Update vektor jika ganti penampilan
```

## 📝 Database Models

### Users (dari SILAB)
```python
id (CHAR 36 - UUID)
name (VARCHAR 255)
email (VARCHAR 255 - unique)
password (VARCHAR 255 - hashed)
created_at, updated_at (TIMESTAMP)
```

### Profile (dari SILAB)
```python
id (CHAR 36 - UUID)
user_id (CHAR 36 - FK to users)
npm (VARCHAR 255)
foto_wajah (VARCHAR 255 - optional)
created_at, updated_at (TIMESTAMP)
```

### PeriodePiket (dari SILAB)
```python
id (CHAR 36 - UUID)
kepengurusan_lab_id (CHAR 36 - FK to kepengurusan_lab) - REQUIRED
nama (VARCHAR 255)
tanggal_mulai (DATE)
tanggal_selesai (DATE)
isactive (BOOLEAN)
created_at, updated_at (TIMESTAMP)
```

### JadwalPiket (dari SILAB)
```python
id (CHAR 36 - UUID)
user_id (CHAR 36 - FK to users)
hari (VARCHAR 255 - Senin/Selasa/...)
kepengurusan_lab_id (CHAR 36 - FK to kepengurusan_lab) - REQUIRED
created_at, updated_at (TIMESTAMP)
```

### Absensi (dari SILAB)
```python
id (CHAR 36 - UUID)
tanggal (DATE)
jam_masuk (TIME)
jam_keluar (TIME - nullable)
foto (VARCHAR 255 - empty string saat mulai)
jadwal_piket (CHAR 36 - FK to jadwal_piket) - NOT user_id!
kegiatan (TEXT - empty string saat mulai, wajib saat akhiri)
periode_piket_id (CHAR 36 - FK to periode_piket)
created_at, updated_at (TIMESTAMP)

CATATAN PENTING:
- Tabel absensi TIDAK memiliki kolom user_id
- User diakses melalui: absensi -> jadwal_piket -> user
- Field jadwal_piket berisi UUID jadwal, bukan user_id
```

### KepengurusanLab (dari SILAB)
```python
id (CHAR 36 - UUID)
tahun_kepengurusan_id (CHAR 36 - FK to tahun_kepengurusan)
laboratorium_id (CHAR 36 - FK to laboratorium)
sk (VARCHAR 255 - Surat Keputusan)
created_at, updated_at (TIMESTAMP)
```

## 🚀 Deployment

### Development
```powershell
python manage.py runserver 0.0.0.0:8000
```

### Production (Example with Gunicorn)
```powershell
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 web_piket.wsgi:application
```

### Environment Variables for Production
```env
DEBUG=False
SECRET_KEY=<generate-strong-random-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
API_PIKET_URL=https://api.yourdomain.com
```

## 📄 License

MIT License

## 👨‍💻 Development

- **Version**: 1.1.0
- **Framework**: Django 5.1.3
- **Integration**: API Piket 3.0.1
- **Last Updated**: November 27, 2025
- **Repository**: https://github.com/Benni2013/web-piket

### Recent Updates (v1.1.0)
- ✅ Fixed `absensi` model structure (removed `user_id` dependency)
- ✅ Added `KepengurusanLab` model for proper foreign key relationships
- ✅ Updated all views to query via `jadwal_piket` instead of direct `user_id`
- ✅ Added dropdown fields for `kepengurusan_lab_id` in forms (periode & jadwal)
- ✅ Fixed field names: `nama_periode` → `nama`, `is_active` → `isactive`
- ✅ Comprehensive `.gitignore` for Django projects

---

## 📞 Support

Jika ada pertanyaan atau issue:
1. Cek dokumentasi API Piket di `../api-piket/README.md`
2. Pastikan API Piket sudah running
3. Test endpoint API dengan curl atau Postman
4. Cek console browser untuk JavaScript errors

---

## 🎉 Quick Start

```powershell
# 1. Clone & Setup
cd web
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure
copy .env.example .env
# Edit .env dengan database credentials

# 3. Run
python manage.py runserver

# 4. Access
# Browser: http://localhost:8000
```

Selamat menggunakan Web Piket SILAB! 🎓
