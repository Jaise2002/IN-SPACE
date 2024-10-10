from django.urls import path
from . import views 

urlpatterns=[
    path('',views.index,name='index'),
      path('Login' , views.user_login , name="Login"),
       path('register' , views.user_register , name="user_register"),
       path('logout',views.user_logout,name='logout'),
       path('manager' , views.manager , name="manager"),
        path('member-tasks/', views.member_tasks, name='member_tasks'),
         path('add-member/', views.add_member, name='add_member'),
         path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
             path('update-task-status/<int:task_id>/', views.update_task_status, name='update_task_status'),
    path('update-progress/', views.update_progress, name='update_progress'),
    path('send-chat/', views.send_chat, name='send_chat'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
]