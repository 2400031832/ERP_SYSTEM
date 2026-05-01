# ERP System - Railway PostgreSQL Setup

## Overview

This ERP system is configured to work with Railway's PostgreSQL database. The application supports multiple user roles:
- **Student** - Access student features
- **Faculty** - Access faculty/teacher features  
- **Admin** - Administrative access
- **Administrator** - Full system administration

## Authentication & Registration

### Sign Up Process

1. Navigate to the login page (`/login` or `/`)
2. Click "Sign Up" to access role-based registration
3. Select your role:
   - **Student Sign Up** - Create a student account
   - **Faculty Sign Up** - Create a faculty account
   - **Admin Sign Up** - Create an admin account
   - **Administrator Sign Up** - Create an administrator account
4. Fill in required information and submit
5. Login with your new credentials

### User Roles

#### Student
- Fill in additional fields:
  - Roll Number
  - Registration Number
  - Date of Birth
  - Department
  - Year & Semester

#### Faculty/Teacher
- Basic registration
- No additional fields required

#### Admin
- Basic registration
- Administrative privileges

#### Administrator
- Basic registration
- Full system administrative access

## Railway PostgreSQL Configuration

The application automatically detects and uses Railway PostgreSQL in production.

### Environment Variables

Railway automatically provides these environment variables:

```
DATABASE_URL          # PostgreSQL connection string
PGHOST               # Database host
PGPORT               # Database port (usually 5432)
PGDATABASE           # Database name
PGUSER               # Database user
PGPASSWORD           # Database password
```

### Local Development

For local development with SQLite (default):
```bash
python manage.py migrate
python manage.py runserver
```

### Production Deployment (Railway)

1. **Create Railway PostgreSQL Service**
   - Go to Railway dashboard
   - Create new PostgreSQL service
   - Link to your ERP application

2. **Environment Variables**
   - Railway automatically provides `DATABASE_URL`
   - Alternatively, provide: `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`

3. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

## Database Schema

### CustomUser Model
- `username` - Unique user identifier
- `email` - User email
- `first_name` - First name
- `last_name` - Last name
- `role` - User role (student, teacher, admin, administrator)
- `phone` - Contact number
- `password` - Hashed password

### Student Model (extends CustomUser)
- `roll_number` - Student roll number
- `registration_number` - Registration number
- `date_of_birth` - Date of birth
- `phone` - Contact number
- `address` - Address
- `department` - Department
- `year` - Academic year
- `semester` - Semester

## Features by Role

### Student Features
- View grades
- Check attendance
- View timetable
- Enroll in courses
- View course materials

### Faculty Features
- Upload grades
- Manage attendance
- Create course materials
- View student list

### Admin Features
- Manage users
- Configure system settings
- Generate reports
- User management

### Administrator Features
- Full system access
- Database management
- Security settings
- System configuration

## Testing

### Test Accounts

After migration, you can create test accounts via:
- Web registration form
- Django admin (`/admin/`)
- Management command

```bash
# Create test student
python manage.py shell
```

```python
from users.models import CustomUser
from students.models import Student

user = CustomUser.objects.create_user(
    username='teststudent',
    email='student@test.com',
    password='testpass123',
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
```

## Troubleshooting

### Database Connection Issues

1. **Railway Connection Error**
   - Verify `DATABASE_URL` environment variable is set
   - Check Railway PostgreSQL service is running
   - Verify credentials in connection string

2. **Migration Errors**
   - Ensure database exists
   - Check permissions: `GRANT ALL PRIVILEGES ON DATABASE erp TO user;`

3. **Role Mismatch Error**
   - Select correct role during login
   - Role must match account creation role

### Production Debugging

Enable debug logging by setting environment variable:
```
DEBUG=true  # Only for troubleshooting
```

## Installation Instructions

### Prerequisites
- Python 3.10+
- pip package manager
- Railway account (for PostgreSQL)

### Setup Steps

1. **Clone Repository**
   ```bash
   git clone <repo-url>
   cd erp_system/ERP_System
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

6. **Access Application**
   - Open browser: http://localhost:8000
   - Login page: http://localhost:8000/login/
   - Register page: http://localhost:8000/register/

## API Endpoints

### Authentication
- `GET/POST /login/` - Login page and authentication
- `GET/POST /register/` - Registration page (role-based)
- `GET /logout/` - Logout user
- `GET /home/` - Dashboard (requires login)

### Students App
- `GET /students/` - Student list
- `GET /students/crud/` - Student CRUD operations
- `GET /courses/` - Course list
- `GET /grades/` - Grade view
- `GET /attendance/` - Attendance tracking

## Security Notes

- Passwords are hashed using Django's default PBKDF2
- CSRF protection enabled
- SQL injection protection via ORM
- Role-based access control implemented
- Connection pooling configured (CONN_MAX_AGE=600)

## Support

For issues or questions:
1. Check logs: `python manage.py check`
2. Review Django documentation: https://docs.djangoproject.com/
3. Railway documentation: https://docs.railway.app/

## License

This project is part of the ERP System.
