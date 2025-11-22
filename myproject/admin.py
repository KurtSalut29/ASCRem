from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Setting, Class, Student, Enrollment, Attendance, Score, GradeSummary, Report, UserSettings


# -----------------------------
# Custom User Admin
# -----------------------------
class UserAdmin(BaseUserAdmin):
    model = User
    ordering = ["instructor_id"]
    list_display = ("instructor_id", "username", "email", "status", "is_active", "is_staff")
    search_fields = ("instructor_id", "username", "email")

    fieldsets = (
        (None, {"fields": ("instructor_id", "username", "password")}),
        ("Personal Info", {"fields": ("email",)}),
        ("Status & Permissions", {
            "fields": (
                "status",
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "instructor_id",
                "email",
                "password1",
                "password2",
                "is_active",
                "is_staff",
            ),
        }),
    )


# -----------------------------
# Custom Class Admin
# -----------------------------
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['class_name', 'subject', 'section', 'instructor', 'get_student_count']
    list_filter = ['instructor', 'section']
    search_fields = ['class_name', 'subject', 'section']
    
    def get_student_count(self, obj):
        return obj.students.count()
    get_student_count.short_description = 'Number of Students'


# -----------------------------
# Custom Student Admin
# -----------------------------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'display_name', 'class_obj', 'program', 'year_level', 'section']
    list_filter = ['class_obj', 'program', 'year_level', 'section', 'academic_year']
    search_fields = ['student_id', 'first_name', 'last_name', 'email']
    list_select_related = ['class_obj']  # Optimize queries
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('photo', 'last_name', 'first_name', 'middle_initial', 'student_id')
        }),
        ('Academic Information', {
            'fields': ('class_obj', 'program', 'year_level', 'section', 'academic_year')
        }),
        ('Contact Information', {
            'fields': ('email', 'contact_number', 'address'),
            'classes': ('collapse',)  # Make this collapsible
        }),
    )


# -----------------------------
# Custom Attendance Admin
# -----------------------------
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'class_obj', 'date', 'status']
    list_filter = ['class_obj', 'status', 'date']
    search_fields = ['student__first_name', 'student__last_name', 'student__student_id']
    date_hierarchy = 'date'
    list_select_related = ['student', 'class_obj']
    
    def get_student_name(self, obj):
        return obj.student.display_name
    get_student_name.short_description = 'Student'


# -----------------------------
# Register Remaining Models
# -----------------------------
admin.site.register(User, UserAdmin)
admin.site.register(Setting)
# Class and Student are registered above with @admin.register decorator
admin.site.register(Enrollment)
# Attendance is registered above with @admin.register decorator
admin.site.register(Score)
admin.site.register(GradeSummary)
admin.site.register(Report)
admin.site.register(UserSettings)