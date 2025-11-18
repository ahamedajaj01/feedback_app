# 📝 Feedback Application (Django + MySQL)

A lightweight Django application for collecting user feedback with authentication, role-based access, and an admin dashboard where admin can see every users feedback.  
Built with Django, MySQL, and Bootstrap 5.

---
## 🌐 Live Demo
https://feedbackapp-production-d50a.up.railway.app

## 🚀 Features

### **User**
- Register / Login / Logout
- Submit feedback (name, email, message)
- View only their own feedback
- Edit or delete their own feedback
- Clean Bootstrap UI

### **Admin**
- Access Django admin panel
- View all submitted feedback
- Cannot access user-only pages
- Automatic redirection to admin feedback list

---

## 🛠 Tech Stack
- **Python**
- **Django**
- **MySQL**
- **Bootstrap 5**

---

## 📂 Project Structure (important parts)
```
project/
│── feedback/                # Django project
│── feedback_app/            # Main app
│── templates/               # HTML templates
│── static/                  # Static assets (CSS/JS/images)
│── .gitignore
│── prod_run.bat             # (safe — no secrets)
│── requirements.txt
```

---

## 🔧 Installation & Setup (Development)

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd project
```

### 2. Create virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables  
Create a `.env` file (NOT committed to git):

```
MYSQL_DATABASE=feedback_db
MYSQL_USER=root
MYSQL_PASSWORD=your_db_password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Apply migrations
```bash
python manage.py migrate
```

### 6. Create admin user
```bash
python manage.py createsuperuser
```

### 7. Run development server
```bash
python manage.py runserver
```

App:  
http://127.0.0.1:8000/  
Admin panel:  
http://127.0.0.1:8000/admin/

---

## 📦 Production Notes (Important)

This project uses **two settings files**:

- `settings.py` (development)
- `prod_settings.py` (production)

To run with production settings on the server:

```
python manage.py runserver 0.0.0.0:8000 --settings=feedback.prod_settings
```

### Production `.env` example:
```env
DJANGO_SECRET_KEY=your-strong-secret
DJANGO_DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

MYSQL_DATABASE=feedback_db
MYSQL_USER=prod_user
MYSQL_PASSWORD=prod_password

SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

⚠️ **Do NOT commit your `.env` file.**

---

## 🗂 Database Model (Summary)
The `Feedback` model stores:
- name  
- email  
- message  
- created timestamp  
- user (ForeignKey)

---

## ✔ Future Enhancements
- Admin search + filters
- Pagination
- Email notifications
- Class-based views
- User profile page

---


