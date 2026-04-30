from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student, Attendance

@login_required
def attendance_view(request):
    try:
        student = Student.objects.get(user=request.user)
        attendances = Attendance.objects.filter(student=student)
        total_conducted = sum(a.total_conducted for a in attendances)
        total_attended = sum(a.total_attended for a in attendances)
        overall = round((total_attended/total_conducted)*100, 1) if total_conducted > 0 else 0
        context = {'student': student, 'attendances': attendances, 'overall': overall, 'is_student': True}
    except Student.DoesNotExist:
        searched_student = None
        attendances = []
        overall = 0
        error = None
        if request.method == 'POST':
            roll = request.POST.get('roll_number', '').strip()
            try:
                searched_student = Student.objects.get(registration_number=roll)
                attendances = Attendance.objects.filter(student=searched_student)
                total_conducted = sum(a.total_conducted for a in attendances)
                total_attended = sum(a.total_attended for a in attendances)
                overall = round((total_attended/total_conducted)*100, 1) if total_conducted > 0 else 0
            except Student.DoesNotExist:
                error = f"No student found with registration number: {roll}"
        context = {'is_admin': True, 'searched_student': searched_student, 'attendances': attendances, 'overall': overall, 'error': error}
    return render(request, 'attendance/attendance.html', context)
