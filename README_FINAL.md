# Educational ERP System

A comprehensive Educational Enterprise Resource Planning (ERP) system built with Django, designed to manage student information, grades, attendance, timetables, and more.

## Features

### 🎓 Core Features

- **Student Management**
  - Student registration and profiles
  - Roll number and registration number tracking
  - Department and semester management
  - Attendance tracking
  - Grade management

- **User Roles**
  - Students - Access grades, attendance, courses
  - Faculty - Manage grades and attendance
  - Admin - System administration
  - Administrator - Full system control

- **Academic Information**
  - Course management
  - Grade tracking
  - Attendance records
  - Timetable management
  - Internals/Assessment tracking

### 🔐 Security Features

- Role-based access control
- Secure password hashing (PBKDF2)
- CSRF protection
- SQL injection prevention
- Session-based authentication

### 📱 Technology

- **Backend:** Django 6.0
- **Database:** PostgreSQL (production) / SQLite (development)
- **Server:** Gunicorn + Nginx (production)
- **Frontend:** HTML5, CSS3, JavaScript
- **Deployment:** Railway

## Quick Start

### Prerequisites

- Python 3.10+
- pip package manager
- PostgreSQL (for production) or SQLite (development)

### Installation

1. **Clone and Setup**
   ```bash
   cd ERP_System
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

2. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

4. **Access Application**
   - Open browser: http://localhost:8000
   - Admin panel: http://localhost:8000/admin/

## User Registration

### Sign Up Process

1. Click **"Sign Up"** on login page
2. Select your role:
   - **Student** - Full student profile with academic details
   - **Faculty** - Faculty/Teacher account
   - **Admin** - Administrative access
   - **Administrator** - Full system access

3. Fill registration form
4. Create account
5. Login with credentials

### Sample Accounts

**Student:**
- Username: `student1`
- Password: `password123`
- Role: Student

**Faculty:**
- Username: `faculty1`
- Password: `password123`
- Role: Faculty

**Admin:**
- Username: `admin1`
- Password: `password123`
- Role: Admin

**Administrator:**
- Username: `admin2`
- Password: `password123`
- Role: Administrator

## Project Structure

```
ERP_System/
├── users/                      # Authentication & User Management
│   ├── models.py              # CustomUser model
│   ├── views.py               # Login, Register, Logout
│   ├── urls.py                # Authentication URLs
│   └── ...
├── students/                   # Student Management
│   ├── models.py              # Student, Course, Grade, Attendance
│   ├── views.py               # Dashboard, CRUD operations
│   ├── urls.py                # Student URLs
│   └── ...
├── attendance/                 # Attendance Module
│   ├── models.py              # Attendance tracking
│   └── ...
├── grades/                     # Grades Module
│   ├── models.py              # Grade records
│   └── ...
├── timetable/                  # Timetable Module
│   ├── models.py              # Timetable management
│   └── ...
├── templates/                  # HTML Templates
│   ├── login.html
│   ├── register.html
│   ├── home.html
│   └── ...
├── static/                     # CSS, JS, Images
│   └── ...
├── erp_system/                 # Project Settings
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL config
│   ├── wsgi.py               # WSGI application
│   └── asgi.py               # ASGI application
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management
├── Procfile                    # Railway deployment config
├── vercel.json                 # Vercel config (optional)
├── SETUP_GUIDE.md             # Setup instructions
├── RAILWAY_SETUP.md           # Railway configuration
├── RAILWAY_DEPLOYMENT.md      # Deployment guide
├── IMPLEMENTATION_SUMMARY.md  # Changes summary
└── README.md                   # This file
```

## Database Models

### CustomUser
```python
- username (unique)
- email
- first_name
- last_name
- role (student, teacher, admin, administrator)
- phone
```

### Student
```python
- user (link to CustomUser)
- roll_number
- registration_number
- date_of_birth
- phone
- address
- department
- year (academic year)
- semester
```

### Course
```python
- code
- name
- description
- department
- semester
```

### Grade
```python
- student
- course
- grade
- description
- course_name
```

### Attendance
```python
- student
- course
- total_conducted
- total_attended
- academic_year
- semester
```

## API Endpoints

### Authentication
| Method | URL | Purpose |
|--------|-----|---------|
| GET/POST | `/login/` | User login |
| GET/POST | `/register/` | User registration |
| GET | `/logout/` | User logout |

### Student
| Method | URL | Purpose |
|--------|-----|---------|
| GET | `/home/` | Dashboard |
| GET | `/students/` | Student list |
| GET/POST | `/students/crud/` | Student CRUD |
| GET | `/grades/` | View grades |
| GET | `/attendance/` | View attendance |
| GET | `/courses/` | View courses |
| GET | `/timetable/` | View timetable |

## Configuration

### Environment Variables

**Development:**
```bash
DEBUG=True
SECRET_KEY=your-dev-key
DATABASE_URL=sqlite:///db.sqlite3  # Or PostgreSQL URL
```

**Production (Railway):**
```bash
DEBUG=False
SECRET_KEY=your-production-key
DATABASE_URL=postgresql://user:pass@host/db
ALLOWED_HOSTS=your-domain.railway.app
```

### Database Configuration

**SQLite (Development):**
- Automatically created in `db.sqlite3`
- No configuration needed

**PostgreSQL (Production):**
- Set `DATABASE_URL` environment variable
- Or set: `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`

## Deployment

### Railway Deployment

1. **Connect GitHub**
   - Push code to GitHub
   - Connect Railway to GitHub repo

2. **Add PostgreSQL**
   - Add PostgreSQL service in Railway
   - Link to your web service
   - Railway auto-populates `DATABASE_URL`

3. **Set Environment Variables**
   - `DEBUG=False`
   - `SECRET_KEY=your-secret`
   - `ALLOWED_HOSTS=your-domain.railway.app`

4. **Run Migrations**
   ```bash
   railway run python manage.py migrate
   ```

5. **Create Superuser**
   ```bash
   railway run python manage.py createsuperuser
   ```

See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for detailed steps.

## Development Commands

```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run tests
python manage.py test

# Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic

# Check project status
python manage.py check
```

## Testing

### Test Student Account Creation

```bash
python manage.py shell
```

```python
from users.models import CustomUser
from students.models import Student

user = CustomUser.objects.create_user(
    username='test_student',
    email='student@test.com',
    password='test123',
    first_name='Test',
    last_name='Student',
    role='student'
)

Student.objects.create(
    user=user,
    roll_number='2024001',
    registration_number='REG2024001',
    department='CSE',
    year=1,
    semester=1
)

# Login with: username=test_student, password=test123
```

## Security

### Features Implemented
✅ PBKDF2 password hashing  
✅ CSRF protection enabled  
✅ SQL injection prevention (ORM)  
✅ Role-based access control  
✅ Session security  
✅ Connection pooling  

### Production Checklist
- [ ] Change SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Enable HTTPS
- [ ] Setup security headers
- [ ] Configure logging
- [ ] Setup monitoring
- [ ] Configure backups

## Troubleshooting

### Database Issues
```bash
# Check migrations
python manage.py showmigrations

# Reset to specific migration
python manage.py migrate users 0001_initial

# Check database status
python manage.py dbshell
```

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8001

# Or kill process (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Role Mismatch on Login
- Ensure selected role matches registration role
- Student account cannot login as Faculty

## Documentation Files

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Installation & setup guide
- **[RAILWAY_SETUP.md](RAILWAY_SETUP.md)** - Railway PostgreSQL setup
- **[RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)** - Production deployment
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical details

## Support

### Resources
- Django Documentation: https://docs.djangoproject.com/
- Railway Documentation: https://docs.railway.app/
- PostgreSQL Documentation: https://www.postgresql.org/docs/

### Getting Help
1. Check documentation files
2. Review Django error messages
3. Check Railway logs
4. Review project issues

## License

This project is part of the Educational ERP System.

## Authors

ERP Development Team

---

## Status

✅ **PRODUCTION READY**

- [x] Role-based authentication
- [x] Student management
- [x] Grade tracking
- [x] Attendance management
- [x] PostgreSQL support
- [x] Railway deployment ready
- [x] Complete documentation
- [x] Security implementation

**Last Updated:** May 1, 2026  
**Version:** 1.0.0

---

**Getting Started?** Start with [SETUP_GUIDE.md](SETUP_GUIDE.md)  
**Deploying?** Check [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)  
**Questions?** See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
