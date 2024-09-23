from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'address', 'phone_number')
    
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'address', 'phone_number')

    
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_name', 'teacher', 'schedule')
    
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'assigned_date', 'due_date')
    
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'assignment', 'student', 'submission_date')
    
@admin.register(AcademicRecord)
class AcademicRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'subject', 'grade')
    
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student','date', 'status')
    
@admin.register(Examination)
class ExaminationAdmin(admin.ModelAdmin):
    list_display = ('id','exam_name', 'subject', 'enrollment_date')
    
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'total_copies')
    
@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('id','book', 'borrow_date', 'return_date')