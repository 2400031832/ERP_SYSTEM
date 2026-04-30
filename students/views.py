
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, Course, Attendance, Grade
from users.models import CustomUser


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        try:
            pw = request.POST.get('password')
            if pw != request.POST.get('password2'):
                messages.error(request, 'Passwords do not match!')
                return render(request, 'register.html')
            username = request.POST.get('registration_number') or request.POST.get('username')
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Registration number already registered!')
                return render(request, 'register.html')
            user = CustomUser.objects.create_user(
                username=username, email=request.POST.get('email'), password=pw,
                first_name=request.POST.get('first_name'), last_name=request.POST.get('last_name'))
            Student.objects.create(
                user=user, roll_number=request.POST.get('registration_number'),
                registration_number=request.POST.get('registration_number'),
                date_of_birth=request.POST.get('date_of_birth'), phone=request.POST.get('phone'),
                address=request.POST.get('address'), department=request.POST.get('department'),
                year=request.POST.get('year'), semester=request.POST.get('semester'))
            messages.success(request, 'Account created! Please login.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home(request):
    try:
        student = Student.objects.get(user=request.user)
        courses = Course.objects.filter(department=student.department, semester=student.semester)
        courses_count = courses.count() or Course.objects.count()
        context = {
            'attendance_count': student.attendances.count(),
            'grades_count': student.grades.count(),
            'courses_count': courses_count,
            'is_student': True, 'student': student,
        }
        return render(request, 'home.html', context)
    except Student.DoesNotExist:
        # Admin/Lecturer dashboard
        total_students = Student.objects.count()
        total_grades = Grade.objects.count()
        total_attendance = Attendance.objects.count()
        from django.db.models import Avg
        low_att = Attendance.objects.filter(total_conducted__gt=0)
        low_att_count = sum(
            1 for a in low_att
            if a.total_attended / a.total_conducted * 100 < 75
        )
        context = {
            'is_admin': True,
            'total_students': total_students,
            'total_grades': total_grades,
            'total_courses': Course.objects.count(),
            'low_attendance_count': low_att_count,
            'recent_students': Student.objects.select_related('user').order_by('-id')[:5],
        }
        return render(request, 'admin_home.html', context)


@login_required
def student_list(request):
    return render(request, 'students/student_list.html', {'students': Student.objects.all()})


@login_required
def student_crud(request):
    students = Student.objects.all()
    selected_student = None
    if request.method == 'POST' and 'read_student' in request.POST:
        selected_student = Student.objects.filter(roll_number=request.POST.get('read_roll_number')).first()
    return render(request, 'students/student_crud.html', {'students': students, 'selected_student': selected_student})


@login_required
def student_create(request):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.create_user(
                username=request.POST.get('username'), email=request.POST.get('email'),
                password='student123', first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'))
            Student.objects.create(
                user=user, roll_number=request.POST.get('roll_number'),
                registration_number=request.POST.get('registration_number'),
                date_of_birth=request.POST.get('date_of_birth'), phone=request.POST.get('phone'),
                address=request.POST.get('address'), department=request.POST.get('department'),
                year=request.POST.get('year'), semester=request.POST.get('semester'))
            messages.success(request, 'Student created!')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return redirect('student_crud')


@login_required
def student_update(request):
    if request.method == 'POST':
        try:
            student = Student.objects.get(roll_number=request.POST.get('update_roll_number'))
            for field in ['phone', 'address', 'department', 'year', 'semester']:
                setattr(student, field, request.POST.get(field))
            student.save()
            student.user.first_name = request.POST.get('first_name')
            student.user.last_name = request.POST.get('last_name')
            student.user.email = request.POST.get('email')
            student.user.save()
            messages.success(request, 'Student updated!')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return redirect('student_crud')


@login_required
def student_delete(request):
    if request.method == 'POST':
        try:
            student = Student.objects.get(roll_number=request.POST.get('delete_roll_number'))
            user = student.user
            student.delete()
            user.delete()
            messages.success(request, 'Student deleted!')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return redirect('student_crud')


@login_required
def attendance(request):
    import random
    years = ['2024-2025', '2025-2026']
    semesters = ['Odd Sem', 'Even Sem']
    academic_year = request.GET.get('academic_year', '')
    semester = request.GET.get('semester', '')
    search_submitted = academic_year != '' and semester != ''

    base_ctx = {
        'years': years, 'semesters': semesters,
        'selected_year': academic_year, 'selected_sem': semester,
        'search_submitted': search_submitted,
        'attendance_data': [],
    }

    if not search_submitted:
        return render(request, 'attendance/attendance.html', base_ctx)

    try:
        student = Student.objects.get(user=request.user)
        att_qs = student.attendances.filter(
            academic_year=academic_year,
            semester=semester,
        )
        if att_qs.exists():
            attendance_data = list(att_qs.values(
                'course_code', 'course_desc', 'ltps', 'section',
                'total_conducted', 'total_attended'
            ))
        else:
            # Generate and seed realistic data
            SUBJECTS = [
                ('24MT2019','PROBABILITY AND STATISTICS','L','S-7-MA'),
                ('24MT2019','PROBABILITY AND STATISTICS','T','S-7-MA'),
                ('24CS01EF','PYTHON FULL STACK DEVELOPMENT','L','S-1-MA'),
                ('24CS01EF','PYTHON FULL STACK DEVELOPMENT','P','S-1-B'),
                ('24CS2203','DESIGN AND ANALYSIS OF ALGORITHMS','L','S-13-MA'),
                ('24CS2203','DESIGN AND ANALYSIS OF ALGORITHMS','P','S-13-B'),
                ('24CS2201','DATABASE MANAGEMENT SYSTEMS','L','S-5-MA'),
                ('24CS2201','DATABASE MANAGEMENT SYSTEMS','P','S-5-B'),
                ('24CS2202','OPERATING SYSTEMS','L','S-9-MA'),
                ('24CS2204','COMPUTER NETWORKS','L','S-11-MA'),
                ('24CS2205','SOFTWARE ENGINEERING','L','S-3-MA'),
            ]
            from students.models import Attendance as Att
            attendance_data = []
            for code, desc, ltps, section in SUBJECTS:
                conducted = random.randint(30, 50)
                pct = random.choice([64, 75, 80, 85, 90, 95, 98, 100])
                attended = int(conducted * pct / 100)
                obj, _ = Att.objects.get_or_create(
                    student=student, course_code=code, ltps=ltps,
                    academic_year=academic_year, semester=semester,
                    defaults={
                        'course_desc': desc, 'section': section,
                        'total_conducted': conducted, 'total_attended': attended,
                    }
                )
                attendance_data.append({
                    'course_code': obj.course_code,
                    'course_desc': obj.course_desc,
                    'ltps': obj.ltps,
                    'section': obj.section,
                    'total_conducted': obj.total_conducted,
                    'total_attended': obj.total_attended,
                })

        return render(request, 'attendance/attendance.html', {
            **base_ctx, 'attendance_data': attendance_data,
        })
    except Student.DoesNotExist:
        return render(request, 'attendance/attendance.html', base_ctx)
def courses_view(request):
    years = ['2024-2025', '2025-2026']
    semesters = ['Odd Sem', 'Even Sem']
    selected_year = request.GET.get('academic_year', '')
    selected_sem = request.GET.get('semester', '')
    search_submitted = selected_year != '' and selected_sem != ''

    try:
        student = Student.objects.get(user=request.user)
        if search_submitted:
            from students.models import Grade
            # Get course codes from grades for selected year/sem
            grade_codes = Grade.objects.filter(
                student=student,
                academic_year=selected_year,
                semester=selected_sem
            ).values_list('course_code', 'course_desc', 'credits')

            # Build course-like list from grade data
            courses_list = [
                {'course_code': code, 'course_name': desc, 'credits': cr,
                 'semester': selected_sem, 'academic_year': selected_year}
                for code, desc, cr in grade_codes
            ]
        else:
            courses_list = []

        return render(request, 'courses/courses.html', {
            'student': student,
            'courses': courses_list,
            'is_student': True,
            'years': years,
            'semesters': semesters,
            'selected_year': selected_year,
            'selected_sem': selected_sem,
            'search_submitted': search_submitted,
        })
    except Student.DoesNotExist:
        return render(request, 'courses/courses.html', {
            'courses': [], 'years': years, 'semesters': semesters,
            'selected_year': selected_year, 'selected_sem': selected_sem,
            'search_submitted': search_submitted,
        })


@login_required
def course_internals(request):
    years = ['2024-2025', '2025-2026']
    semesters = ['Odd Sem', 'Even Sem']
    academic_year = request.GET.get('academic_year', '')
    semester = request.GET.get('semester', '')
    search_submitted = academic_year != '' and semester != ''

    base_ctx = {
        'years': years, 'semesters': semesters,
        'selected_year': academic_year, 'selected_sem': semester,
        'search_submitted': search_submitted,
    }

    try:
        student = Student.objects.get(user=request.user)
        if search_submitted:
            from students.models import Grade
            grade_qs = Grade.objects.filter(
                student=student,
                academic_year=academic_year,
                semester=semester,
            ).values('course_code', 'course_desc', 'credits')
            courses = list(grade_qs)
        else:
            courses = []
        return render(request, 'courses/internals.html', {
            **base_ctx, 'courses': courses, 'student': student,
        })
    except Student.DoesNotExist:
        return render(request, 'courses/internals.html', {**base_ctx, 'courses': []})


@login_required
def grades(request):
    academic_year = request.GET.get('academic_year', '')
    semester = request.GET.get('semester', '')
    search_submitted = academic_year != '' and semester != ''

    years = ['2024-2025', '2025-2026']
    semesters = ['Odd Sem', 'Even Sem']

    if not search_submitted:
        return render(request, 'grades/grades.html', {
            'grades': [],
            'search_submitted': False,
            'academic_year': academic_year,
            'semester': semester,
            'total_courses': 0,
            'total_credits': 0,
            'sgpa': 0,
            'years': years,
            'semesters': semesters,
            'selected_year': academic_year,
            'selected_sem': semester,
            'records': [],
            'cgpa': 0,
            'total_credits': 0,
        })

    try:
        student = Student.objects.get(user=request.user)

        # Seed grades if empty
        if not student.grades.exists():
            GRADE_DATA = [
                ('24MT2019','PROBABILITY AND STATISTICS',3,22,48),
                ('24CS01EF','PYTHON FULL STACK DEVELOPMENT',4,25,52),
                ('24CS2203','DESIGN AND ANALYSIS OF ALGORITHMS',3,20,45),
                ('24CS2201','DATABASE MANAGEMENT SYSTEMS',3,28,55),
                ('24CS2202','OPERATING SYSTEMS',3,21,50),
                ('24CS2204','COMPUTER NETWORKS',3,19,42),
                ('24CS2205','SOFTWARE ENGINEERING',3,24,48),
            ]
            for code, name, cr, internal, external in GRADE_DATA:
                course = Course.objects.filter(course_code=code).first()
                Grade.objects.create(
                    student=student, course=course, course_code=code, course_desc=name,
                    credits=cr, internal_marks=internal, external_marks=external,
                    academic_year='2025-2026', semester='Even Sem')

        records = student.grades.all()
        years = records.values_list('academic_year', flat=True).distinct()
        semesters = records.values_list('semester', flat=True).distinct()
        if academic_year:
            records = records.filter(academic_year=academic_year)
        if semester:
            records = records.filter(semester=semester)

        # Calculate SGPA
        cgpa = None
        total_credits = 0
        if records.exists():
            weighted = sum(g.grade_points * g.credits for g in records)
            total_credits = sum(g.credits for g in records)
            cgpa = round(weighted / total_credits, 2) if total_credits else 0

        return render(request, 'grades/grades.html', {
            'records': records, 'years': years, 'semesters': semesters,
            'selected_year': academic_year, 'selected_sem': semester,
            'cgpa': cgpa, 'total_credits': total_credits, 'search_submitted': True,
        })
    except Student.DoesNotExist:
        return render(request, 'grades/grades.html', {'records': [], 'years': ['2024-2025','2025-2026'], 'semesters': ['Odd Sem','Even Sem'], 'search_submitted': False, 'cgpa': 0, 'total_credits': 0, 'selected_year': '', 'selected_sem': ''})


@login_required
def update_internals(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('home')

    years = ['2024-2025', '2025-2026']
    selected_roll = request.GET.get('roll', '')
    selected_year = request.GET.get('year', '')
    selected_sem  = request.GET.get('sem', '')
    selected_student = None
    courses = []

    if selected_roll:
        try:
            selected_student = Student.objects.select_related('user').get(roll_number=selected_roll)
            qs = selected_student.grades.all()
            if selected_year:
                qs = qs.filter(academic_year=selected_year)
            if selected_sem:
                qs = qs.filter(semester=selected_sem)
            courses = list(qs.order_by('academic_year','semester','course_code'))
        except Student.DoesNotExist:
            pass

    if request.method == 'POST' and selected_roll:
        from django.contrib import messages as msg_mod
        grade_pk = request.POST.get('grade_pk')
        component = request.POST.get('component', '')
        internal_marks = request.POST.get('internal_marks')
        try:
            selected_student = Student.objects.select_related('user').get(roll_number=selected_roll)
            g = Grade.objects.get(pk=int(grade_pk), student=selected_student)
            new_internal = float(internal_marks)
            total = new_internal + g.external_marks
            def compute_grade(t):
                if t >= 90: return ('O', 10)
                elif t >= 80: return ('A+', 9)
                elif t >= 70: return ('A', 8)
                elif t >= 60: return ('B+', 7)
                elif t >= 50: return ('B', 6)
                elif t >= 40: return ('C', 5)
                else: return ('F', 0)
            grade, gp = compute_grade(total)
            Grade.objects.filter(pk=g.pk).update(
                internal_marks=new_internal,
                total_marks=total,
                grade=grade,
                grade_points=gp,
            )
            msg_mod.success(request, f'Updated {component} for {g.course_code} — new total: {total}, grade: {grade}')
            qs = selected_student.grades.all()
            if selected_year: qs = qs.filter(academic_year=selected_year)
            if selected_sem: qs = qs.filter(semester=selected_sem)
            courses = list(qs.order_by('academic_year','semester','course_code'))
        except Exception as e:
            from django.contrib import messages as msg_mod2
            msg_mod2.error(request, f'Error: {e}')

    return render(request, 'students/update_internals.html', {
        'years': years,
        'selected_roll': selected_roll,
        'selected_year': selected_year,
        'selected_sem': selected_sem,
        'selected_student': selected_student,
        'courses': courses,
    })
