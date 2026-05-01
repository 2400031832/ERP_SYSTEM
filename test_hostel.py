#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_system.settings')
django.setup()

from students.models import Hostel, Student
from django.contrib.auth import get_user_model

User = get_user_model()

try:
    # Try to get the test user and student
    user = User.objects.get(username='teststudent')
    student = Student.objects.get(user=user)
    
    print(f"Student: {student.roll_number}")
    print(f"Student hostel: {student.hostel}")
    
    # Try to generate a random hostel
    random_data = Hostel.generate_random_hostel()
    print(f"Random hostel data generated successfully")
    print(f"Hostel name: {random_data['hostel_name']}")
    
    # Try to create a hostel
    hostel, created = Hostel.objects.get_or_create(
        hostel_name=random_data['hostel_name'],
        defaults=random_data
    )
    print(f"Hostel created: {created}")
    print(f"Hostel: {hostel.hostel_name}")
    print(f"Hostel amenities: {hostel.amenities}")
    print("SUCCESS")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
