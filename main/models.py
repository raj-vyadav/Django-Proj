from django.contrib.auth.models import User
from django.db import models

# Student Model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Links to User model
    roll_no = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    year = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username if self.user else "Unknown Student"

# Teacher Model
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Links to User model
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username if self.user else "Unknown Teacher"

# Attendance Model
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Links to Student model
    date = models.DateField()
    status = models.BooleanField()
    class Meta:
        unique_together = ('student', 'date')  # Prevent duplicate attendance for the same student and date

    def __str__(self):
        return f"{self.student.user.username} | {self.date}"

# Marks Model
class Marks(models.Model):
   student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Links to Student model
   subject = models.CharField(max_length=100)
   marks_obtained = models.FloatField()
   total_marks = models.FloatField()

   class Meta:
      unique_together = ('student', 'subject')  
   def __str__(self):
      return f"{self.student.user.username} - {self.subject}: {self.marks_obtained}/{self.total_marks}"
