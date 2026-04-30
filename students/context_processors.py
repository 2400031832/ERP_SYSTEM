from .models import Student

def sidebar_students(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        students = Student.objects.select_related('user').order_by('roll_number')
        return {'sidebar_students': students}
    return {'sidebar_students': []}
