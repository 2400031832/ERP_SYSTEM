from django.db import models
from django.conf import settings


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    registration_number = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    department = models.CharField(max_length=100)
    year = models.IntegerField()
    semester = models.IntegerField()
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.roll_number} - {self.user.get_full_name()}"


class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=200)
    credits = models.IntegerField(default=3)
    department = models.CharField(max_length=100)
    semester = models.IntegerField()
    academic_year = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    course_code = models.CharField(max_length=20)
    course_desc = models.CharField(max_length=100)
    ltps = models.CharField(max_length=1, choices=[('L','L'),('T','T'),('P','P'),('S','S')])
    section = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=20)
    semester = models.CharField(max_length=20)
    total_conducted = models.IntegerField(default=0)
    total_attended = models.IntegerField(default=0)

    @property
    def total_absent(self):
        return self.total_conducted - self.total_attended

    @property
    def percentage(self):
        if self.total_conducted == 0:
            return 0
        return round((self.total_attended / self.total_conducted) * 100, 1)

    def __str__(self):
        return f"{self.student} - {self.course_code}"


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    course_code = models.CharField(max_length=20)
    course_desc = models.CharField(max_length=200)
    credits = models.IntegerField(default=3)
    internal_marks = models.FloatField(default=0)
    external_marks = models.FloatField(default=0)
    total_marks = models.FloatField(default=0)
    grade = models.CharField(max_length=5, blank=True)
    grade_points = models.FloatField(default=0)
    academic_year = models.CharField(max_length=20)
    semester = models.CharField(max_length=20)

    def calculate_grade(self):
        total = self.internal_marks + self.external_marks
        self.total_marks = total
        if total >= 90: self.grade, self.grade_points = 'O', 10.0
        elif total >= 80: self.grade, self.grade_points = 'A+', 9.0
        elif total >= 70: self.grade, self.grade_points = 'A', 8.0
        elif total >= 60: self.grade, self.grade_points = 'B+', 7.0
        elif total >= 50: self.grade, self.grade_points = 'B', 6.0
        else: self.grade, self.grade_points = 'F', 0.0

    def save(self, *args, **kwargs):
        self.calculate_grade()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.course_code} - {self.grade}"
