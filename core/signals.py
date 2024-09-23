from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Student, Teacher

@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:  # Assuming staff are teachers
            Teacher.objects.create(user=instance)
        else:
            Student.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user(sender, instance, **kwargs):
    if hasattr(instance, 'student'):
        instance.studentprofile.save()
    if hasattr(instance, 'teacher'):
        instance.teacherprofile.save()