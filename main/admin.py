from django.contrib import admin
from .models import Student, Teacher, Attendance, Marks
# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Attendance)
admin.site.register(Marks)
# admin.site.register(Post)