from django.urls import path
from .import views

urlpatterns = [
   path('', views.home, name='home'),
   path('home', views.home, name='home'),
   path('teacher_dashboard', views.teacher_dashboard, name='teacher_dashboard'),
   path('student_dashboard', views.student_dashboard, name='student_dashboard'),
   path('attendance', views.view_attendance, name='view_attendance'),
   path('marks', views.view_marks, name='view_marks'),
   path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
   path('add_marks', views.add_marks, name='add_marks'),
   # path('add_student', views.add_student, name='add_student'),
   # path('add_student', views.add_student, name='add_student'),
   # path('post_delete/<str:pk>/', views.post_delete, name='post_delete'),
   # path('user_ban/<str:user_id>/', views.user_ban, name='user_ban'),
   # path('user_unban/<str:user_id>/', views.user_unban, name='user_unban'),
   path('sign_up/', views.sign_up, name='sign_up'),
   ]