# ERP System Setup Instructions

## Project Structure

```
ERP_System/
├── erp_system/          # Main project settings
├── users/               # Authentication & user management
├── students/            # Student management & main views
├── attendance/          # Attendance tracking
├── grades/              # Grade management
├── timetable/           # Timetable management
├── templates/           # HTML templates
├── static/              # CSS, JS, images
├── manage.py            # Django management
└── requirements.txt     # Dependencies
```

## Quick Start

### 1. Installation

```bash
# Navigate to project directory
cd ERP_System

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

#### Local Development (SQLite)
```bash
# Apply migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

#### Production (Railway PostgreSQL)
```bash
# Set environment variables for Railway PostgreSQL
export DATABASE_URL="postgresql://user:pass@host:port/dbname"

# Or use individual variables:
export PGHOST="host.railway.app"
export PGPORT="5432"
export PGDATABASE="railway"
export PGUSER="postgres"
export PGPASSWORD="your-password"

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files for production
python manage.py collectstatic --noinput

# Run with gunicorn
gunicorn erp_system.wsgi:application --bind 0.0.0.0:8000
```

### 3. Access Application

- **Login/Register**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **Home**: http://localhost:8000/home/

## User Registration Flow

### Step 1: Access Registration
Click "Sign Up" on the login page and select your role

### Step 2: Role-Based Registration

#### Student Registration
- First Name, Last Name, Email
- Username, Password
- Roll Number, Registration Number
- Department, Year, Semester
- Date of Birth (optional)

#### Faculty Registration
- First Name, Last Name, Email
- Username, Password
- Phone (optional)

#### Admin/Administrator Registration
- First Name, Last Name, Email
- Username, Password
- Phone (optional)

### Step 3: Login
- Use your username and password
- Select the same role you registered with
- Click "Sign In"

## Features by Role

### Student Dashboard
- View grades
- Check attendance
- Browse courses
- View timetable

### Faculty Dashboard
- Upload grades
- Mark attendance
- Create course materials
- Manage students

### Admin Dashboard
- User management
- System configuration
- Generate reports
- Data management

### Administrator Dashboard
- Full system control
- Database management
- Security configuration
- All features

## Database Models

### CustomUser (extends Django User)
```python
- username: str (unique)
- email: str
- first_name: str
- last_name: str
- role: choice (student, teacher, admin, administrator)
- phone: str (optional)
```

### Student
```python
- user: ForeignKey to CustomUser
- roll_number: str
- registration_number: str
- date_of_birth: date (optional)
- phone: str
- address: str
- department: str
- year: int
- semester: int
```

## Environment Variables

### Development
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3 (or PostgreSQL URL)
```

### Production (Railway)
```
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://...
ALLOWED_HOSTS=your-domain.railway.app
```

## Common Commands

```bash
# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Clear cache
python manage.py clear_cache

# Check project status
python manage.py check
```

## Troubleshooting

### "Port 8000 already in use"
```bash
# Use different port
python manage.py runserver 8001

# Or kill the process using port 8000
# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

### "No migrations to apply"
```bash
# Check migration status
python manage.py showmigrations

# Create new migrations if needed
python manage.py makemigrations
python manage.py migrate
```

### "Database does not exist"
```bash
# PostgreSQL - Create database
createdb -U postgres erp_system

# Or connect and create in PostgreSQL
psql -U postgres
CREATE DATABASE erp_system;
```

### Role mismatch error during login
- Make sure you select the same role during login as during registration
- Student account cannot login as Faculty

## Testing

### Create Test Data

```bash
python manage.py shell
```

```python
from users.models import CustomUser
from students.models import Student

# Create test student
user = CustomUser.objects.create_user(
    username='student1',
    email='student@test.com',
    password='password123',
    first_name='John',
    last_name='Doe',
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

# Create test faculty
faculty = CustomUser.objects.create_user(
    username='faculty1',
    email='faculty@test.com',
    password='password123',
    first_name='Jane',
    last_name='Smith',
    role='teacher'
)
```

## Security Notes

✓ Passwords hashed with PBKDF2
✓ CSRF protection enabled
✓ SQL injection prevention via ORM
✓ Role-based access control
✓ Connection pooling for database

⚠️ Change SECRET_KEY in production
⚠️ Set DEBUG=False in production
⚠️ Use HTTPS in production
⚠️ Keep dependencies updated

## Support & Documentation

- Django: https://docs.djangoproject.com/
- Railway: https://docs.railway.app/
- PostgreSQL: https://www.postgresql.org/docs/
- Project Wiki: Check the repository

## License

This project is part of the Educational ERP System.
