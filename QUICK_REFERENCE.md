# Quick Reference Guide

## 🚀 Get Started in 2 Minutes

### Step 1: Setup
```bash
cd ERP_System
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Step 2: Access
- Open: http://localhost:8000/login/
- Default: Sign up as Student/Faculty/Admin/Administrator

---

## 📚 Key URLs

| URL | Purpose |
|-----|---------|
| `/login/` | Login page |
| `/register/?role=student` | Student sign up |
| `/register/?role=faculty` | Faculty sign up |
| `/register/?role=admin` | Admin sign up |
| `/register/?role=administrator` | Administrator sign up |
| `/logout/` | Logout |
| `/home/` | Dashboard |
| `/admin/` | Django admin |

---

## 👥 User Roles

### Student
- Create account with roll number
- View grades and attendance
- Access courses

### Faculty
- Manage student grades
- Track attendance
- Update course information

### Admin
- System administration
- User management
- Report access

### Administrator
- Full system access
- All admin features
- Database access

---

## 🔑 Test Accounts

**Already Created? Use:**
```
Username: student1
Password: password123
Role: Student
```

**Want to Create New?**
1. Click "Sign Up" on login page
2. Select role
3. Fill form
4. Create account
5. Login

---

## 📝 Test Student Registration

```bash
# Option 1: Via Web
URL: http://localhost:8000/register/?role=student
Fill form and submit

# Option 2: Via Shell
python manage.py shell

from users.models import CustomUser
from students.models import Student

user = CustomUser.objects.create_user(
    username='newstudent',
    email='student@example.com',
    password='test123',
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
```

---

## 🗄️ Database Status

```bash
# Check migrations
python manage.py showmigrations users
# Output: [X] 0001_initial
#         [X] 0002_alter_customuser_role

# Verify database
python manage.py dbshell
```

---

## 📱 PostgreSQL Configuration

### Development (SQLite)
- Auto-configured
- File: `db.sqlite3`
- No setup needed

### Production (PostgreSQL)
- Set `DATABASE_URL` environment variable
- Or set: `PGHOST`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`
- Rails auto-configures in Railway

---

## 🚢 Deploy to Railway

```bash
# 1. Push code
git push origin main

# 2. Railway auto-deploys

# 3. Run migrations
railway run python manage.py migrate

# 4. Create superuser
railway run python manage.py createsuperuser

# 5. Access app
https://your-app.railway.app
```

---

## 🛠️ Common Commands

```bash
# Check system
python manage.py check

# Database operations
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations

# Create admin
python manage.py createsuperuser

# Run server
python manage.py runserver

# Django shell
python manage.py shell

# Static files
python manage.py collectstatic

# Run tests
python manage.py test
```

---

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8000 in use | `python manage.py runserver 8001` |
| Migrations failed | `python manage.py migrate --fake` then `python manage.py migrate` |
| Database error | Check PostgreSQL running, verify credentials |
| Role mismatch | Login with same role used at registration |
| Module not found | `pip install -r requirements.txt` |

---

## 📊 Project Structure

```
ERP_System/
├── users/               # Authentication ✅
├── students/           # Student management
├── attendance/         # Attendance tracking
├── grades/             # Grade management
├── timetable/          # Timetable management
├── templates/          # HTML files
├── static/             # CSS, JS, Images
├── erp_system/         # Settings & config
├── manage.py
└── requirements.txt
```

---

## ✅ What's Ready

- ✅ Student sign-up with role
- ✅ Faculty sign-up with role
- ✅ Admin sign-up with role
- ✅ Administrator sign-up with role
- ✅ Secure login with role validation
- ✅ PostgreSQL database support
- ✅ Railway deployment ready
- ✅ Complete documentation

---

## 📖 Documentation

- `README_FINAL.md` - Full project overview
- `SETUP_GUIDE.md` - Installation & setup
- `RAILWAY_SETUP.md` - PostgreSQL setup
- `RAILWAY_DEPLOYMENT.md` - Deploy to production
- `IMPLEMENTATION_SUMMARY.md` - Technical details
- `COMPLETION_SUMMARY.md` - What was done

---

## 🎯 Next Steps

1. **Test Locally**
   ```bash
   python manage.py runserver
   # Visit http://localhost:8000/login/
   ```

2. **Create Test User**
   - Sign up as Student
   - Login with credentials
   - Verify data saved

3. **Deploy to Railway**
   - Connect GitHub
   - Set environment variables
   - Push code

4. **Customize** (Optional)
   - Edit forms
   - Add more fields
   - Customize templates

---

## 💡 Pro Tips

1. **Always use virtual environment**
   ```bash
   source venv/bin/activate  # or venv\Scripts\activate
   ```

2. **Check errors first**
   ```bash
   python manage.py check
   ```

3. **Test registration before deploy**
   - Create test account locally
   - Verify data saved
   - Test login

4. **Use Railway for PostgreSQL**
   - Free tier available
   - Auto-backups
   - Monitoring included

---

## 🆘 Need Help?

1. Check documentation files
2. Run `python manage.py check`
3. Review error messages
4. Check Django logs
5. See troubleshooting section above

---

## 🎉 Success Indicators

✅ Django check passes (0 issues)  
✅ Migrations applied successfully  
✅ Server runs on http://localhost:8000  
✅ Can sign up with different roles  
✅ Can login with correct credentials  
✅ Role mismatch prevents wrong-role login  
✅ User data saved in database  

**If all above pass → SYSTEM IS WORKING! 🎊**

---

## 📞 Support

- **Setup Issues:** See `SETUP_GUIDE.md`
- **Deployment:** See `RAILWAY_DEPLOYMENT.md`
- **Technical:** See `IMPLEMENTATION_SUMMARY.md`
- **General:** See `README_FINAL.md`

---

**Version:** 1.0.0  
**Last Updated:** May 1, 2026  
**Status:** ✅ PRODUCTION READY
