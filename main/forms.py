from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    # Add custom fields
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[('teacher', 'Teacher'), ('student', 'Student')], required=True, label="Role")

    # Optional fields for students or teachers
    roll_no = forms.CharField(required=False, label="Roll Number (Students Only)")
    year = forms.CharField(required=False, label="Year (Students Only)")
    department = forms.CharField(required=True, label="Department")
    teacher_id = forms.CharField(required=False, label="Teacher ID (Teachers Only)")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Save email to User model
        if commit:
            user.save()
        return user

class AddStudentForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")
    roll_no = forms.CharField(max_length=20, label="Roll Number")
    department = forms.CharField(max_length=100, label="Department")
