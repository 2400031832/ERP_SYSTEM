from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('students.urls')),
    path('attendance/', include('attendance.urls')),
    path('grades/', include('grades.urls')),
    path('timetable/', include('timetable.urls')),
]
