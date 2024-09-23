from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import Usermanager
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class User(AbstractUser):
    phone_number= models.CharField(max_length=10)
    email= models.EmailField(unique=True)
    otp= models.PositiveIntegerField(null=True, blank=True)
    # USER_TYPE_CHOICES={
    #     'student', 'Student',
    #     'teacher', 'Teacher',
    # }
    # user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    
    USERNAME_FIELD="email"
    REQUIRED_FIELDS = [
        "first_name", "last_name", "phone_number"
        ]
    
    
    objects=Usermanager()
    
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    class_name = models.CharField(max_length=20)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.user.username} - Student"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    subject = models.CharField(max_length=100)
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - Teacher"
    
    
    
@receiver(post_save, sender=User)
def create_student(sender, instance, created, **kwargs):
    if created and hasattr(instance, 'student'):
        Student.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_student(sender, instance, **kwargs):
    if hasattr(instance, 'student'):
        instance.student.save()