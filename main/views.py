import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required, permission_required
from .models import Attendance, Marks, Student, Teacher
from django.contrib.auth.models import User, Group
from django.contrib import messages  # To fix the import error for messages
# from .utils import generate_random_password

# Home View
@login_required(login_url='/login')
def home(request):
    if request.user.groups.filter(name='Teachers').exists():
        return redirect('teacher_dashboard')
    elif request.user.groups.filter(name='Students').exists():
        return redirect('student_dashboard')
    return render(request, 'main/home.html')

# Sign-Up View

def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Create a User instance but don't save to the database yet
                user = form.save(commit=False)  
                user.first_name = form.cleaned_data.get("first_name")
                user.last_name = form.cleaned_data.get("last_name")
                user.save()  # Now save to the database
                
                # Get the role (student or teacher)
                role = form.cleaned_data.get("role")
                if role == "student":
                    # Assign the user to the 'Students' group
                    student_group, created = Group.objects.get_or_create(name='Students')
                    user.groups.add(student_group)

                    # Create the Student profile
                    Student.objects.create(
                        user=user,
                        roll_no=form.cleaned_data.get("roll_no"),
                        department=form.cleaned_data.get("department"),
                        year=form.cleaned_data.get("year"),
                    )
                elif role == "teacher":
                    # Assign the user to the 'Teachers' group
                    teacher_group, created = Group.objects.get_or_create(name='Teachers')
                    user.groups.add(teacher_group)

                    # Create the Teacher profile
                    Teacher.objects.create(
                        user=user,
                        department=form.cleaned_data.get("department"),
                    )

                # Success message and redirect
                messages.success(request, "Registration successful!")
                return redirect('/login')
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
        else:
            messages.error(request, "Invalid form data. Please correct the errors.")
    else:
        form = RegistrationForm()
    
    return render(request, 'registration/sign_up.html', {'form': form})

# Mark Attendance View
@login_required(login_url='/login')
@permission_required('main.add_attendance', login_url='/login', raise_exception=True)
def mark_attendance(request):
    if not request.user.groups.filter(name='Teachers').exists():
        return redirect('home')  # Prevent non-teachers from accessing

    students = Student.objects.all()
    attendance_list = Attendance.objects.all()  # Fetch all attendance records

    if request.method == 'POST':
        student_user_id = request.POST.get('student_user_id')
        date = datetime.date.today()  # Current date
        status = request.POST.get('status') == "Present"  # Convert "Present" to True, otherwise False

        # Fetch the User and Student objects
        user = get_object_or_404(User, id=student_user_id)
        student = get_object_or_404(Student, user=user)

        # Check for duplicate attendance for the same date
        if Attendance.objects.filter(student=student, date=date).exists():
            messages.error(request, f"Attendance for {student.user.get_full_name()} on {date} already exists!")
        else:
            # Create new attendance record
            Attendance.objects.create(student=student, date=date, status=status)
            messages.success(request, f"Attendance marked for {student.user.get_full_name()} as {'Present' if status else 'Absent'}.")

    return render(request, 'main/mark_attendance.html', {'students': students, 'attendance_list': attendance_list})


# Teacher Dashboard View
def teacher_dashboard(request):
    teacher_data = get_object_or_404(Teacher, user=request.user)
    return render(request, 'main/teacher_dashboard.html', {'teacher_data': teacher_data})

# Student Dashboard View
def student_dashboard(request):
    student_data = get_object_or_404(Student, user=request.user)
    return render(request, 'main/student_dashboard.html', {'student_data': student_data})

# View Attendance
@login_required(login_url='/login')
def view_attendance(request):
    if request.user.groups.filter(name='Students').exists():
        # Fetch attendance for the logged-in student
        attendances = Attendance.objects.filter(student=request.user.student)
    else:
        # Fetch all attendance records for non-students (e.g., teachers)
        attendances = Attendance.objects.all()
    return render(request, 'main/view_attendance.html', {'attendances': attendances})

# View Marks
@login_required(login_url='/login')
def view_marks(request):
    if request.user.groups.filter(name='Students').exists():
        # Fetch marks for the logged-in student
        marks = Marks.objects.filter(student=request.user.student)
        return render(request, 'main/view_marks.html', {'marks': marks})
    else:
        return redirect('home')  # Redirect non-students to home
    
@login_required(login_url='/login')
@permission_required('main.add_marks', login_url='/login', raise_exception=True)
def add_marks(request):
    if not request.user.groups.filter(name='Teachers').exists():
        return redirect('home')  # Restrict access to teachers

    students = Student.objects.all()
    marks_list = Marks.objects.all()  # Fetch existing marks to display

    if request.method == 'POST':
        errors = []
        has_processed_any = False  # Flag to check if any student data was processed

        for student in students:
            # Check if the checkbox for this student is selected
            if request.POST.get(f"select_student_{student.user.id}"):
                has_processed_any = True  # At least one checkbox is selected
                subject = request.POST.get(f"subject_{student.user.id}")
                marks_obtained = request.POST.get(f"marks_obtained_{student.user.id}")
                total_marks = request.POST.get(f"total_marks_{student.user.id}")

                # Validate the input fields
                if not subject or not marks_obtained or not total_marks:
                    errors.append(f"Missing data for {student.user.get_full_name()}. Please fill all fields.")
                    continue

                try:
                    # Check for duplicate records
                    if Marks.objects.filter(student=student, subject=subject).exists():
                        errors.append(f"Marks for {student.user.get_full_name()} in {subject} already exist!")
                    else:
                        Marks.objects.create(
                            student=student,
                            subject=subject,
                            marks_obtained=float(marks_obtained),
                            total_marks=float(total_marks)
                        )
                except Exception as e:
                    errors.append(f"An error occurred for {student.user.get_full_name()}: {e}")

        # If no checkbox was selected, raise an error
        if not has_processed_any:
            messages.error(request, "No students were selected. Please select at least one checkbox.")
        elif errors:
            # If there were any errors during processing, display them
            for error in errors:
                messages.error(request, error)
        else:
            # If everything was processed successfully
            messages.success(request, "Marks added successfully for the selected students!")

    return render(request, 'main/add_marks.html', {'students': students, 'marks_list': marks_list})
