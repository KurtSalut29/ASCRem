from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import random
import string
from django.utils import timezone
from datetime import timedelta

# -----------------------------
# Custom User Model
# -----------------------------
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)  # Override with no validators
    instructor_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    middle_name = models.CharField(max_length=30, blank=True)
    department = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    # ✅ Login with instructor_id instead of username
    USERNAME_FIELD = 'instructor_id'
    REQUIRED_FIELDS = ['username', 'email']

    groups = models.ManyToManyField(
        "auth.Group",
        blank=True,
        related_name="custom_user_set"
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        blank=True,
        related_name="custom_user_set"
    )

    @property
    def full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip()

    def __str__(self):
        return f"{self.username} ({self.instructor_id})"


# -----------------------------
# Email Verification Model
# -----------------------------
class EmailVerification(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)
    
    @classmethod
    def generate_code(cls):
        return ''.join(random.choices(string.digits, k=6))
    
    def __str__(self):
        return f"{self.email} - {self.code}"


# -----------------------------
# Class Model
# -----------------------------
class Class(models.Model):
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    program = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    year_level = models.CharField(max_length=20)
    section = models.CharField(max_length=50)
    semester = models.CharField(max_length=20)
    school_year = models.CharField(max_length=20)

    @property
    def class_name(self):
        """Generate class name from program, subject, year_level, and section."""
        return f"{self.program} - {self.subject} ({self.year_level} - {self.section})"
    
    def __str__(self):
        return f"{self.program} - {self.subject} ({self.year_level} - {self.section})"


# -----------------------------
# Student Model
# -----------------------------
class Student(models.Model):
    class_obj = models.ForeignKey(Class, related_name="students", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="students/photos/", blank=True, null=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_initial = models.CharField(max_length=50, blank=True, null=True)
    student_id = models.CharField(max_length=20, unique=True)
    program = models.CharField(max_length=100)
    year_level = models.CharField(max_length=20)
    section = models.CharField(max_length=50)
    academic_year = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # -----------------------------
    # Display full name as Lastname, Firstname Middlename (blank if no middle)
    # -----------------------------
    @property
    def display_name(self):
        """Return the student's name as Lastname, Firstname Middlename (blank if middle is None)."""
        middle = f" {self.middle_initial}." if self.middle_initial else ""
        return f"{self.last_name}, {self.first_name}{middle}"

    # -----------------------------
    # For admin or string representation
    # -----------------------------
    def __str__(self):
        return self.display_name

# -----------------------------
# Enrollment
# -----------------------------
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'class_obj')

    def __str__(self):
        return f"{self.student} → {self.class_obj}"


# -----------------------------
# Attendance
# -----------------------------
class Attendance(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[
            ("Present", "Present"),
            ("Absent", "Absent"),
            ("Late", "Late"),
            ("Excused", "Excused")
        ]
    )

    class Meta:
        unique_together = ('class_obj', 'student', 'date')

    def __str__(self):
        return f"{self.student.full_name} - {self.date} ({self.status})"


# -----------------------------
# Score (Legacy)
# -----------------------------
class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    quiz1 = models.FloatField(default=0)
    quiz2 = models.FloatField(default=0)
    quiz3 = models.FloatField(default=0)
    assignment = models.FloatField(default=0)
    project = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    final_grade = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.class_obj}: {self.final_grade}"


# -----------------------------
# Grade Calculation Settings
# -----------------------------
class GradeCalculationSettings(models.Model):
    class_obj = models.OneToOneField(Class, on_delete=models.CASCADE, related_name='grade_settings')
    quiz_percentage = models.FloatField(default=30.0)
    assignment_percentage = models.FloatField(default=20.0)
    project_percentage = models.FloatField(default=20.0)
    exam_percentage = models.FloatField(default=30.0)
    attendance_percentage = models.FloatField(default=0.0)
    passing_grade = models.FloatField(default=75.0)
    
    def __str__(self):
        return f"Grade Settings for {self.class_obj}"


# -----------------------------
# Grade Summary
# -----------------------------
class GradeSummary(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    equivalent_grade = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)  # Add this
    final_grade = models.FloatField()
    remarks = models.CharField(max_length=10, choices=[("Passed", "Passed"), ("Failed", "Failed")])
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.full_name} - {self.final_grade} ({self.remarks})"


# -----------------------------
# Report
# -----------------------------
class Report(models.Model):
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    generated_on = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Report for {self.class_obj} ({self.generated_on.date()})"


# -----------------------------
# Setting (per user)
# -----------------------------
class Setting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="app_setting")
    notification_pref = models.CharField(
        max_length=20,
        choices=[("email", "Email"), ("sms", "SMS"), ("none", "None")],
        default="email"
    )
    theme = models.CharField(max_length=50, default="light")
    auto_generate_report = models.BooleanField(default=False)
    default_report_format = models.CharField(
        max_length=10,
        choices=[("pdf", "PDF"), ("excel", "Excel"), ("print", "Print")],
        default="pdf"
    )
    school_year = models.CharField(max_length=20, default="25-1", help_text="Current active school year (e.g., 25-1)")
    password_updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings for {self.user.full_name}"


# -----------------------------
# User Settings (Profile)
# -----------------------------
class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    notifications_enabled = models.BooleanField(default=True)
    theme = models.CharField(
        max_length=20,
        choices=[("Light", "Light"), ("Dark", "Dark")],
        default="Light"
    )

    def __str__(self):
        return f"Profile for {self.user.full_name}"


# -----------------------------
# Activity Log
# -----------------------------
class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    class_obj = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.action} ({self.timestamp})"


# ============================================================
# 🆕 NEW MODELS for Dynamic Grading System
# ============================================================

# -----------------------------
# Grade Category (Quiz, Activity, Exam, etc.)
# -----------------------------
class GradeCategory(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="grade_categories")
    name = models.CharField(max_length=50)
    percentage = models.FloatField(help_text="Percentage weight of this category")

    def __str__(self):
        return f"{self.name} ({self.percentage}%) - {self.class_obj}"


# -----------------------------
# Grade Item (e.g., Quiz #1, Exam #1, etc.)
# -----------------------------
class GradeItem(models.Model):
    category = models.ForeignKey(GradeCategory, on_delete=models.CASCADE, related_name="items")
    item_name = models.CharField(max_length=100)
    total_items = models.IntegerField(default=0)
    passing_percentage = models.FloatField(default=0)

    def __str__(self):
        return f"{self.item_name} ({self.category.name})"


# -----------------------------
# Student Score per Item
# -----------------------------
class StudentScore(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="scores")
    item = models.ForeignKey(GradeItem, on_delete=models.CASCADE, related_name="student_scores")
    score_percentage = models.FloatField(default=0)

    class Meta:
        unique_together = ('student', 'item')

    def __str__(self):
        return f"{self.student.display_name} - {self.item.item_name}: {self.score_percentage}%"



# -----------------------------
# Transmutation Table (Optional)
# -----------------------------
class TransmutationTable(models.Model):
    min_percentage = models.FloatField()
    max_percentage = models.FloatField()
    equivalent_grade = models.FloatField()

    def __str__(self):
        return f"{self.min_percentage}-{self.max_percentage}% → {self.equivalent_grade}"
