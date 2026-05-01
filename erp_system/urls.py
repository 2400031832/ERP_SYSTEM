from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='login', permanent=False), name='root'),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('students.urls')),
    path('attendance/', include('attendance.urls')),
    path('grades/', include('grades.urls')),
    path('timetable/', include('timetable.urls')),
]
