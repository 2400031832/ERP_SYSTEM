from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from students.models import Student, Grade, Course

@login_required
def grades_view(request):
    try:
        student = Student.objects.get(user=request.user)
        grades = Grade.objects.filter(student=student)
        total_credits = sum(g.credits for g in grades)
        total_points = sum(g.grade_points * g.credits for g in grades)
        cgpa = round(total_points/total_credits, 2) if total_credits > 0 else 0
        context = {'student': student, 'grades': grades, 'cgpa': cgpa, 'is_student': True}
    except Student.DoesNotExist:
        courses = Course.objects.all()
        searched_student = None
        student_grades = []
        error = None
        if request.method == 'POST' and 'search_student' in request.POST:
            roll = request.POST.get('roll_number', '').strip()
            try:
                searched_student = Student.objects.get(registration_number=roll)
                student_grades = Grade.objects.filter(student=searched_student)
            except Student.DoesNotExist:
                error = f"No student found with registration number: {roll}"
        if request.method == 'POST' and 'save_marks' in request.POST:
            roll = request.POST.get('roll_number', '').strip()
            cid = request.POST.get('course_id')
            internal = float(request.POST.get('internal_marks', 0))
            external = float(request.POST.get('external_marks', 0))
            ayear = request.POST.get('academic_year', '2025-2026')
            sem = request.POST.get('semester', '5')
            try:
                searched_student = Student.objects.get(registration_number=roll)
                course = get_object_or_404(Course, id=cid)
                grade_obj, created = Grade.objects.get_or_create(
                    student=searched_student, course_code=course.course_code,
                    defaults={'course_desc': course.course_name, 'credits': course.credits, 'academic_year': ayear, 'semester': sem}
                )
                grade_obj.internal_marks = internal
                grade_obj.external_marks = external
                grade_obj.credits = course.credits
                grade_obj.course_desc = course.course_name
                grade_obj.academic_year = ayear
                grade_obj.semester = sem
                grade_obj.save()
                messages.success(request, f'Marks saved for {searched_student.user.get_full_name()} - {course.course_code}!')
                student_grades = Grade.objects.filter(student=searched_student)
            except Student.DoesNotExist:
                error = f"No student found with registration number: {roll}"
        context = {'is_admin': True, 'courses': courses, 'searched_student': searched_student, 'student_grades': student_grades, 'error': error}
    return render(request, 'grades/grades.html', context)
