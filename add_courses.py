import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_system.settings')
django.setup()

from students.models import Course

courses = [
    {'code': '24CS01EF', 'name': 'PYTHON FULL STACK DEVELOPMENT', 'credits': 4, 'dept': 'Computer Science', 'sem': 5, 'year': '2025-2026'},
    {'code': '24CS2201', 'name': 'DATABASE MANAGEMENT SYSTEMS', 'credits': 3, 'dept': 'Computer Science', 'sem': 5, 'year': '2025-2026'},
    {'code': '24CS2202', 'name': 'OPERATING SYSTEMS', 'credits': 3, 'dept': 'Computer Science', 'sem': 5, 'year': '2025-2026'},
    {'code': '24CS2203', 'name': 'DESIGN AND ANALYSIS OF ALGORITHMS', 'credits': 4, 'dept': 'Computer Science', 'sem': 5, 'year': '2025-2026'},
    {'code': '24CS2204', 'name': 'COMPUTER NETWORKS', 'credits': 3, 'dept': 'Computer Science', 'sem': 5, 'year': '2025-2026'},
    {'code': '24CS2205', 'name': 'SOFTWARE ENGINEERING', 'credits': 3, 'dept': 'Computer Science', 'sem': 5, 'year': '2025-2026'},
    {'code': '24MT2019', 'name': 'PROBABILITY AND STATISTICS', 'credits': 3, 'dept': 'Computer Science', 'sem': 5, 'year': '2025-2026'},
]

for c in courses:
    course, created = Course.objects.get_or_create(
        course_code=c['code'],
        defaults={'course_name': c['name'], 'credits': c['credits'], 'department': c['dept'], 'semester': c['sem'], 'academic_year': c['year']}
    )
    print(f"{'✓ Created' if created else 'Exists'}: {c['code']} - {c['name']}")

print(f"\nTotal Courses: {Course.objects.count()}")
