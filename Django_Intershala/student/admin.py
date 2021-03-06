from django.contrib import admin

# Register your models here.
from student.models import Student
from .models import *

admin.site.register(Student)
admin.site.register(StudentApplication)
