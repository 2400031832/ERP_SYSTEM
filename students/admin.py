from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import csv
import io
from .models import Student, Grade, Attendance, Course
from django.contrib.auth import get_user_model

User = get_user_model()


# ── Inline: Grades inside Student ──────────────────────────────────────────
class GradeInline(admin.TabularInline):
    model = Grade
    extra = 0
    fields = ['academic_year', 'semester', 'course_code', 'course_desc',
              'credits', 'internal_marks', 'external_marks', 'total_marks',
              'grade', 'grade_points']
    ordering = ['academic_year', 'semester']


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    fields = ['academic_year', 'semester', 'course_code', 'course_desc',
              'ltps', 'total_conducted', 'total_attended']
    ordering = ['academic_year', 'semester']


# ── Student Admin ───────────────────────────────────────────────────────────
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'full_name', 'department', 'year',
                    'semester', 'grade_count', 'view_link']
    search_fields = ['roll_number', 'registration_number',
                     'user__first_name', 'user__last_name', 'user__username']
    list_filter = ['department', 'year', 'semester']
    inlines = [GradeInline, AttendanceInline]
    readonly_fields = ['roll_number']

    def full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    full_name.short_description = 'Name'

    def grade_count(self, obj):
        return obj.grades.count()
    grade_count.short_description = 'Grades'

    def view_link(self, obj):
        return format_html(
            '<a href="{}" target="_blank">View Profile</a>',
            f'/admin/students/student/{obj.pk}/change/'
        )
    view_link.short_description = 'Admin'


# ── Grade Admin ─────────────────────────────────────────────────────────────
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student_roll', 'student_name', 'academic_year',
                    'semester', 'course_code', 'course_desc', 'credits',
                    'internal_marks', 'external_marks', 'total_marks',
                    'grade', 'grade_points']
    list_editable = ['internal_marks', 'external_marks',
                     'total_marks', 'grade', 'grade_points']
    list_filter = ['academic_year', 'semester', 'grade', 'student__department']
    search_fields = ['student__roll_number', 'course_code', 'course_desc',
                     'student__user__first_name', 'student__user__last_name']
    ordering = ['student__roll_number', 'academic_year', 'semester']
    list_per_page = 50

    def student_roll(self, obj):
        return obj.student.roll_number
    student_roll.short_description = 'Roll No'

    def student_name(self, obj):
        return obj.student.user.get_full_name() or obj.student.user.username
    student_name.short_description = 'Student'

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('upload-internals/',
                 self.admin_site.admin_view(self.upload_internals_view),
                 name='grade_upload_internals'),
        ]
        return custom + urls

    def upload_internals_view(self, request):
        """CSV upload: roll_number,course_code,internal_marks"""
        if request.method == 'POST' and request.FILES.get('csv_file'):
            f = request.FILES['csv_file']
            decoded = f.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded))
            updated, errors = 0, []
            for row in reader:
                try:
                    roll = row['roll_number'].strip()
                    code = row['course_code'].strip()
                    marks = int(row['internal_marks'].strip())
                    ay = row.get('academic_year', '2025-2026').strip()
                    sem = row.get('semester', 'Odd Sem').strip()
                    student = Student.objects.get(roll_number=roll)
                    grade_obj, created = Grade.objects.get_or_create(
                        student=student,
                        course_code=code,
                        academic_year=ay,
                        semester=sem,
                        defaults={'course_desc': code, 'credits': 3,
                                  'internal_marks': marks, 'external_marks': 0,
                                  'total_marks': marks, 'grade': '-',
                                  'grade_points': 0}
                    )
                    if not created:
                        grade_obj.internal_marks = marks
                        grade_obj.total_marks = marks + grade_obj.external_marks
                        grade_obj.save()
                    updated += 1
                except Exception as e:
                    errors.append(f"Row {row}: {e}")

            if errors:
                messages.warning(request, f"Updated {updated} records. Errors: {'; '.join(errors[:5])}")
            else:
                messages.success(request, f"Successfully updated {updated} internal marks!")
            return redirect('..')

        context = {
            'title': 'Upload Internal Marks (CSV)',
            'opts': self.model._meta,
            'has_permission': True,
            'sample': 'roll_number,course_code,internal_marks,academic_year,semester\n2400030008,24CS2201,28,2025-2026,Odd Sem',
        }
        return render(request, 'admin/grade_upload.html', context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['upload_url'] = 'upload-internals/'
        return super().changelist_view(request, extra_context)


# ── Attendance Admin ────────────────────────────────────────────────────────
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student_roll', 'student_name', 'academic_year',
                    'semester', 'course_code', 'course_desc',
                    'total_conducted', 'total_attended', 'percentage']
    list_editable = ['total_conducted', 'total_attended']
    list_filter = ['academic_year', 'semester', 'student__department']
    search_fields = ['student__roll_number', 'course_code',
                     'student__user__first_name']
    ordering = ['student__roll_number', 'course_code']
    list_per_page = 50

    def student_roll(self, obj):
        return obj.student.roll_number
    student_roll.short_description = 'Roll No'

    def student_name(self, obj):
        return obj.student.user.get_full_name() or obj.student.user.username
    student_name.short_description = 'Student'

    def percentage(self, obj):
        if obj.total_conducted:
            pct = round(obj.total_attended / obj.total_conducted * 100, 1)
            color = '#2e7d32' if pct >= 75 else '#c62828'
            return format_html('<b style="color:{}">{} %</b>', color, pct)
        return '-'
    percentage.short_description = 'Attendance %'


# ── Course Admin ────────────────────────────────────────────────────────────
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'course_name', 'credits',
                    'department', 'semester', 'academic_year']
    search_fields = ['course_code', 'course_name']
    list_filter = ['department', 'academic_year', 'semester']
    list_editable = ['credits']

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Grade)
def recalculate_grade_on_save(sender, instance, **kwargs):
    """Auto-update total_marks and grade when admin saves a Grade record."""
    total = instance.internal_marks + instance.external_marks
    def compute(t):
        if t >= 90: return ('O', 10)
        elif t >= 80: return ('A+', 9)
        elif t >= 70: return ('A', 8)
        elif t >= 60: return ('B+', 7)
        elif t >= 50: return ('B', 6)
        elif t >= 40: return ('C', 5)
        else: return ('F', 0)
    grade, gp = compute(total)
    if instance.total_marks != total or instance.grade != grade or instance.grade_points != gp:
        Grade.objects.filter(pk=instance.pk).update(
            total_marks=total, grade=grade, grade_points=gp
        )
