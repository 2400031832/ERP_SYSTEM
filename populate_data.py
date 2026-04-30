import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_system.settings')
django.setup()

from users.models import CustomUser
from students.models import Student, Attendance, Grade
from datetime import date

students_data = [
    {'username': 'john_doe', 'first_name': 'John', 'last_name': 'Doe', 'email': 'john@klu.edu', 'roll': 'CS2024001', 'reg': 'REG001', 'dept': 'Computer Science', 'year': 3, 'sem': 5, 'phone': '9876543210', 'address': 'Vijayawada', 'dob': date(2003, 5, 15)},
    {'username': 'jane_smith', 'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane@klu.edu', 'roll': 'CS2024002', 'reg': 'REG002', 'dept': 'Computer Science', 'year': 3, 'sem': 5, 'phone': '9876543211', 'address': 'Guntur', 'dob': date(2003, 8, 22)},
    {'username': 'raj_kumar', 'first_name': 'Raj', 'last_name': 'Kumar', 'email': 'raj@klu.edu', 'roll': 'CS2024003', 'reg': 'REG003', 'dept': 'Computer Science', 'year': 3, 'sem': 5, 'phone': '9876543212', 'address': 'Hyderabad', 'dob': date(2003, 3, 10)},
    {'username': 'priya_reddy', 'first_name': 'Priya', 'last_name': 'Reddy', 'email': 'priya@klu.edu', 'roll': 'IT2024001', 'reg': 'REG004', 'dept': 'Information Technology', 'year': 2, 'sem': 3, 'phone': '9876543213', 'address': 'Tirupati', 'dob': date(2004, 7, 18)},
    {'username': 'arun_kumar', 'first_name': 'Arun', 'last_name': 'Kumar', 'email': 'arun@klu.edu', 'roll': 'CS2024004', 'reg': 'REG005', 'dept': 'Computer Science', 'year': 3, 'sem': 5, 'phone': '9876543214', 'address': 'Vijayawada', 'dob': date(2003, 11, 5)},
]

attendance_data = [
    {'code': 'CS301', 'desc': 'Python Full Stack', 'ltps': 'L', 'section': 'A', 'conducted': 45, 'attended': 42},
    {'code': 'CS302', 'desc': 'Java Programming', 'ltps': 'L', 'section': 'A', 'conducted': 40, 'attended': 38},
    {'code': 'CS303', 'desc': 'Computer Networks', 'ltps': 'L', 'section': 'A', 'conducted': 35, 'attended': 30},
    {'code': 'CS304', 'desc': 'Mathematics', 'ltps': 'L', 'section': 'A', 'conducted': 38, 'attended': 35},
    {'code': 'CS305', 'desc': 'CIS', 'ltps': 'L', 'section': 'A', 'conducted': 42, 'attended': 40},
]

grades_data = [
    {'code': 'CS301', 'desc': 'Python Full Stack', 'credits': 4, 'internal': 28, 'external': 62, 'total': 90, 'grade': 'O', 'points': 10.0},
    {'code': 'CS302', 'desc': 'Java Programming', 'credits': 3, 'internal': 25, 'external': 55, 'total': 80, 'grade': 'A+', 'points': 9.0},
    {'code': 'CS303', 'desc': 'Computer Networks', 'credits': 3, 'internal': 22, 'external': 48, 'total': 70, 'grade': 'A', 'points': 8.0},
    {'code': 'CS304', 'desc': 'Mathematics', 'credits': 4, 'internal': 26, 'external': 58, 'total': 84, 'grade': 'A+', 'points': 9.0},
    {'code': 'CS305', 'desc': 'CIS', 'credits': 3, 'internal': 24, 'external': 52, 'total': 76, 'grade': 'A', 'points': 8.0},
]

print("Creating students...")
for s in students_data:
    try:
        user, created = CustomUser.objects.get_or_create(username=s['username'], defaults={
            'email': s['email'], 'first_name': s['first_name'], 'last_name': s['last_name']
        })
        if created:
            user.set_password('student123')
            user.save()
        
        student, created = Student.objects.get_or_create(roll_number=s['roll'], defaults={
            'user': user, 'registration_number': s['reg'], 'date_of_birth': s['dob'],
            'phone': s['phone'], 'address': s['address'], 'department': s['dept'],
            'year': s['year'], 'semester': s['sem']
        })
        
        if created:
            for a in attendance_data:
                Attendance.objects.create(
                    student=student, course_code=a['code'], course_desc=a['desc'],
                    ltps=a['ltps'], section=a['section'], academic_year='2024-25',
                    semester=str(s['sem']), total_conducted=a['conducted'], total_attended=a['attended']
                )
            for g in grades_data:
                Grade.objects.create(
                    student=student, course_code=g['code'], course_desc=g['desc'],
                    credits=g['credits'], internal_marks=g['internal'], external_marks=g['external'],
                    total_marks=g['total'], grade=g['grade'], grade_points=g['points'],
                    academic_year='2024-25', semester=str(s['sem'])
                )
            print(f"✓ Created: {s['roll']} - {s['first_name']} {s['last_name']}")
        else:
            print(f"Already exists: {s['roll']}")
    except Exception as e:
        print(f"Error: {e}")

print(f"\nTotal Students: {Student.objects.count()}")
print("Done!")
