from django.urls import path  # type: ignore
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    
    # Class Management
    path("classes/", views.class_panel, name="class_panel"),
    path("classes/<int:class_id>/", views.class_detail, name="class_detail"),
    path("student/<int:student_id>/", views.student_detail, name="student_detail"),

    # Auth
    path("verify-email/", views.verify_email, name="verify_email"),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # Panels
    path("register/", views.register, name="register"),
    path("instructor/", views.instructor_panel, name="instructor_panel"),
    # path("students/", views.student_panel, name="student_panel"),
    path("grades/", views.grades_panel, name="grades_panel"),
    path("profile/", views.profile_view, name="profile"),
    # path("score/", views.score_input, name="score_input"),
    path("class/add/", views.add_class, name="add_class"),
    path("class/<int:class_id>/edit/", views.edit_class, name="edit_class"),
    path("class/<int:class_id>/delete/", views.delete_class, name="delete_class"),
    # path("grades/add_score/", views.add_score, name="add_score"),
    # path("grades/settings/<int:class_id>/", views.update_grade_settings, name="grade_settings"),
    # path("grades/calculate/<int:class_id>/", views.calculate_grades, name="calculate_grades"),
    path("class/<int:class_id>/add-student/", views.add_student, name="add_student"),
    path("student/<int:student_id>/edit/", views.edit_student, name="edit_student"),
    path("student/<int:student_id>/delete/", views.delete_student, name="delete_student"),
    path("classes/", views.class_list, name="class_list"),  # ✅ this name must match
    
    # Attendance Management
    path("attendance/", views.attendance_panel, name="attendance_panel"),
    path("attendance/update/", views.update_attendance, name="update_attendance"),
    path("attendance/summary/<int:class_id>/", views.attendance_summary, name="attendance_summary"),
    
    # Profile and Settings
    path("profile/", views.profile_view, name="profile"),
    path("settings/", views.settings_view, name="settings"),
    
    # CSV Upload
    path("class/<int:class_id>/upload-csv/", views.upload_students_csv, name="upload_csv"),
    
    # Activity Log
    path("activity-log/", views.activity_log, name="activity_log"),
    
    # About Page
    path("about/", views.about_view, name="about"),
    
    # Reports
    path("reports/", views.reports_panel, name="reports_panel"),
    path("reports/attendance/<int:class_id>/", views.generate_attendance_report, name="attendance_report"),
    path("reports/grades/<int:class_id>/", views.generate_grade_report, name="grade_report"),
    path("reports/summary/<int:class_id>/", views.generate_class_summary, name="class_summary"),
    # PDF and Excel Reports
    path("reports/attendance/<int:class_id>/pdf/", views.generate_attendance_pdf, name="attendance_pdf"),
    path("reports/attendance/<int:class_id>/excel/", views.generate_attendance_excel, name="attendance_excel"),
    path("reports/grades/<int:class_id>/pdf/", views.generate_grades_pdf, name="grades_pdf"),
    path("reports/grades/<int:class_id>/excel/", views.generate_grades_excel, name="grades_excel"),
    path("reports/summary/<int:class_id>/pdf/", views.generate_summary_pdf, name="summary_pdf"),
    path("reports/summary/<int:class_id>/excel/", views.generate_summary_excel, name="summary_excel"),
    # Data Export
    path("export/all-data/", views.export_all_data, name="export_all_data"),
    path("attendance/update-ajax/", views.update_attendance_ajax, name="update_attendance_ajax"),



]
