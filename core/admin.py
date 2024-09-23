from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UA
from .models import User
from .models import Student, Teacher

# Register your models here.


@admin.register(User)
class UserAdmin(UA):
    pass

admin.site.register(Student)
admin.site.register(Teacher)