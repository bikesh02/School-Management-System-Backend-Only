from django.db import models
from datetime import date
# from django.contrib.auth.models import User



# Create your models here.

class Student(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name=models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    academic_records = models.TextField()
    enrollment_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.first_name + " " + self.last_name
    


class Teacher(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    availability = models.TextField()
    enrollment_date=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.first_name + " " + self.last_name
    
class Class(models.Model):
    class_name = models.CharField(max_length=150)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    schedule = models.TextField()
    enrollment_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.class_name
    
class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="assignments")
    assigned_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name="assignments_created")
    students_submitted = models.ManyToManyField(Student, through='Submission', related_name="assignments_submitted")
    
    def __str__(self):
        return self.title


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submission_date = models.DateField(auto_now_add=True)
    file_submission = models.FileField(upload_to='submissions/')
    grade = models.CharField(max_length=5, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.assignment.title}"
    
class AcademicRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=150)
    grade = models.CharField(max_length=10)
    remarks = models.TextField()
    enrollment_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.student.first_name + " " + self.student.last_name + " " + self.subject
    
    
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20)
    enrollment_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.student.first_name + " " + self.student.last_name + " " + self.date.strftime('%Y-%m-%d')
    

class Examination(models.Model):
    exam_name = models.CharField(max_length=150)
    date = models.DateField()
    subject = models.CharField(max_length=100)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.exam_name} {self.date.strftime('%Y-%m-%d')} {self.subject}"
    
    
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Student, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.borrower}"
    
    def save(self, *args, **kwargs):
        if self.return_date:
            self.is_returned = True
            self.book.available_copies += 1
        else:
            self.book.available_copies -= 1
        self.book.save()
        super().save(*args, **kwargs)