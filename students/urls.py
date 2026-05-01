from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('students/crud/', views.student_crud, name='student_crud'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/update/', views.student_update, name='student_update'),
    path('students/delete/', views.student_delete, name='student_delete'),
    path('attendance/', views.attendance, name='attendance'),
    path('courses/', views.courses_view, name='courses'),
    path('courses/internals/', views.course_internals, name='course_internals'),
    path('grades/', views.grades, name='grades'),
    path('internals/update/', views.update_internals, name='update_internals'),
]