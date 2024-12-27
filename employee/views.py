from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.utils.datetime_safe import datetime
from employee.models import Employee

def home(request):
    return render(request, 'home.html', {'user': request.user})

def employee_details(request):
    employees = Employee.objects.all()
    return render(request, 'employee_details.html', {'employees':employees})

def add_employee(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        department = request.POST['department']
        role = request.POST['role']
        location = request.POST['location']

        new_emp = Employee(first_name=first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone, department=department,
                           role=role, location=location, hire_date=datetime.now())
        new_emp.save()
        return render(request,'employee_added_successfully.html')
    elif request.method == 'GET':
        return render(request, 'add_employee.html')
    else:
        return HttpResponse('An exception occurred! Employee not added!')

def delete_employee(request, emp_id=0):
    if emp_id:
        try:
            employee_to_delete = Employee.objects.get(id=emp_id)
            employee_to_delete.delete()
            return render(request,'employee_removed_successfully.html')
        except Employee.DoesNotExist:
            return HttpResponse("Employee with the given ID does not exist")
    employees = Employee.objects.all()
    return render(request, 'delete_employee.html', {'employees':employees})

def filter_employee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        department = request.POST.get('department')
        role = request.POST.get('role')

        employees = Employee.objects.all()
        if name:
            employees = employees.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if department:
            employees = employees.filter(department__icontains=department)
        if role:
            employees = employees.filter(role__icontains=role)
        return render(request, 'employee_details.html', {'employees':employees})
    elif request.method == 'GET':
        return render(request, 'filter_employee.html')
    else:
        return HttpResponse("An exception occurred")

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        email=email.lower().strip()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'User does not exist'})

        user = authenticate(username=user.username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        email = email.lower().strip()
        if User.objects.filter(Q(username=name) | Q(email=email)).exists():
            return render(request, 'signup.html', {'msg':'User already exists'})
        else:
            user1 = User.objects.create_user(username=name, email=email, password=password)
            user1.save()
            return redirect('login')  # Redirect to login after successful signup
    else:
        return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('home')
