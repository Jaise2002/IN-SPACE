from django.shortcuts import render
from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.hashers import make_password
from .models import Task



from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, Progress, Chat  # Assuming your models are named Task, Progress, and Chat

@login_required
def update_task_status(request, task_id):
    if request.method == "POST":
        status = request.POST.get('status')
        task = get_object_or_404(Task, id=task_id)
        task.status = status  # Assuming you have a 'status' field in your Task model
        task.save()
        return redirect('your_tasks')  # Redirect to the tasks page


def update_progress(request):
    if request.method == "POST":
        progress_text = request.POST.get('progress')
        # Assuming you have a Progress model linked to User
        Progress.objects.create(user=request.user, text=progress_text)
        return redirect('your_tasks')  # Redirect to the tasks page


def send_chat(request):
    if request.method == "POST":
        message = request.POST.get('message')
        # Assuming you have a Chat model to handle messages
        Chat.objects.create(user=request.user, message=message)
        return redirect('your_tasks')  # Redirect to the tasks page

# Create your views here.
def index(request):
    return render(request,"index.html")

def manager_dashboard(request):
    tasks = Task.objects.all()  # Get all tasks
    progress_updates = Progress.objects.select_related('user').all()  # Get all progress updates
    chat_messages = Chat.objects.select_related('user').all()  # Get all chat messages

    context = {
        'tasks': tasks,
        'progress_updates': progress_updates,
        'chat_messages': chat_messages,
    }
    return render(request, 'manager_dashboard.html', context)

def manager(request):
    active_users = User.objects.filter(is_active=True, is_staff=False, is_superuser=False)

    # Handle task addition
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        member_username = request.POST.get('member')
        
        # Create the task (assuming you have a Task model)
        member = User.objects.get(member=member_username)
        Task.objects.create(name=task_name, member= member)
        return redirect('manager')  # Redirect to the same manager page to see the updated list

    tasks = Task.objects.all()  # Get all tasks for display
    return render(request, "todolist_manager.html", {'active_users': active_users, 'tasks': tasks})

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('manager')

def add_member(request):
    if request.method == 'POST':
        member_name = request.POST.get('member_name')
        User.objects.create(username=member_name, is_active=True)  # Adjust according to your needs
        return redirect('manager')  # Redirect to the manager page

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None and user.is_active:
            if user.is_superuser==False and user.is_staff==True:
                login(request,user)
                return redirect('manager')
            elif user.is_superuser==False and user.is_staff==False:
                login(request,user)
                return redirect('member_tasks')
        elif user is None:
            msg = "Wrong credentials. Please try again!"
            return render(request , 'login.html' , {'msg':msg})
    return render(request , 'login.html')




def member_tasks(request):
    # Get tasks assigned to the logged-in user
    tasks = Task.objects.filter(member=request.user)
    return render(request, "member_tasks.html", {'tasks': tasks})

# def user_register(request):
#     if request.method=='POST':
#         username=request.POST['name']
#         if User.objects.filter(username=username).exists():
#             msg = 'username already exists!'
#             return render(request, 'register.html',{'msg':msg})
#         else:
#             email=request.POST['email']
#             password=request.POST['password']
#             interest=request.POST['interest']
#             new_password = make_password(password)
#             if interest=='Manager':
#                 a=True
#                 User.objects.create(username=username,email=email,password=new_password,is_staff=a)
#                 return redirect('index.html')
#             else:
#                 a=False
#                 User.objects.create(username=username,email=email,password=new_password,is_staff=a)
#                 return redirect('index.html')
        
            
#     return render(request, 'register.html')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'register.html')

        # Create new user
        user = User(
            username=username,
            email=email,
            password=make_password(password),  # Hash the password
           # Set is_staff based on interest
        )
        user.save()
        messages.success(request, 'Registration successful. You can now log in!')
        return redirect('Login')  # Redirect to the login page after successful registration

    return render(request, 'register.html')



def user_logout(request):
    logout(request)
    return redirect('Login')