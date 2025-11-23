from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, Class, Student, Attendance, Score, GradeCalculationSettings
import re  # ✅ Regex import

class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        validators=[],  # Remove all built-in validators
        widget=forms.TextInput(attrs={"placeholder": "Enter Username (letters, numbers, spaces, symbols allowed)"})
    )
    instructor_id = forms.CharField(
        max_length=20,
        required=True,
        label="Instructor ID",
        widget=forms.TextInput(attrs={"placeholder": "Enter Instructor ID (letters, numbers, hyphens allowed)"})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Enter Email"})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter First Name"})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter Last Name"})
    )
    middle_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Enter Middle Name"})
    )
    department = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter Department"})
    )

    # ✅ Password: must be exactly 4 digits
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter 4-digit Password",
            "minlength": "4",
            "maxlength": "4"
        }),
        help_text="Password must be exactly 4 digits (numbers only)."
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm 4-digit Password",
            "minlength": "4",
            "maxlength": "4"
        })
    )

    class Meta:
        model = User
        fields = ["username", "instructor_id", "email", "first_name", "last_name", "middle_name", "department", "password1", "password2"]

    # ✅ Validate 4-digit numeric password
    def clean_password1(self):
        password = self.cleaned_data.get("password1")

        if not re.fullmatch(r"\d{4}", password):
            raise ValidationError("Password must be exactly 4 digits (numbers only).")

        return password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_instructor_id(self):
        instructor_id = self.cleaned_data.get("instructor_id")
        if User.objects.filter(instructor_id=instructor_id).exists():
            raise forms.ValidationError("This Instructor ID is already taken.")
        return instructor_id

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.status = "active"
        if commit:
            user.save()
        return user
    
class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['subject','program', 'year_level', 'section', 'semester', 'school_year']
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'e.g., Web Development'}),
            'program': forms.TextInput(attrs={'placeholder': 'e.g., Bachelor of Science in Information Technology'}),
            'year_level': forms.Select(choices=[
                ('', 'Select Year Level'),
                ('1st Year', '1st Year'),
                ('2nd Year', '2nd Year'),
                ('3rd Year', '3rd Year'),
                ('4th Year', '4th Year'),
            ], attrs={'class': 'form-select'}),
            'section': forms.TextInput(attrs={'placeholder': 'e.g., A, B, C'}),
            'semester': forms.Select(choices=[
                ('', 'Select Semester'),
                ('1st Semester', '1st Semester'),
                ('2nd Semester', '2nd Semester'),
                ('Summer', 'Summer'),
            ], attrs={'class': 'form-select'}),
            'school_year': forms.TextInput(attrs={'placeholder': 'e.g., 25-1'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not self.instance.pk:  # Only for new classes
            try:
                user_setting = user.app_setting
                self.fields['school_year'].initial = user_setting.school_year
            except:
                pass


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "photo",
            "last_name",
            "first_name",
            "middle_initial",
            "student_id",
            "program",
            "year_level",
            "section",
            "academic_year",
            "address",
            "contact_number",
            "email",
        ]

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'status']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'})
        }

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['student', 'quiz1', 'quiz2', 'quiz3', 'assignment', 'project', 'exam']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'quiz1': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'quiz2': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'quiz3': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'assignment': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'project': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'exam': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
        }

class GradeCalculationSettingsForm(forms.ModelForm):
    class Meta:
        model = GradeCalculationSettings
        fields = ['quiz_percentage', 'assignment_percentage', 'project_percentage', 'exam_percentage', 'attendance_percentage', 'passing_grade']
        widgets = {
            'quiz_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '100'}),
            'assignment_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '100'}),
            'project_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '100'}),
            'exam_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '100'}),
            'attendance_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '100'}),
            'passing_grade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '100'}),
        }

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='Upload CSV File',
        help_text='Upload a CSV file with student data.',
        widget=forms.ClearableFileInput(
            attrs={
                'id': 'csvFileInput',
                'accept': '.csv, .xlsx, .xls',
                'hidden': 'hidden'
            }
        )
    )



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'department', 'email', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
