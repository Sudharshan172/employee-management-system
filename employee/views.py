from django.shortcuts import render

# Create your views here.
from lib2to3.fixes.fix_input import context

from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime

from employee.models import Employee


# Create your views here.
def home(request):
    return render(request, 'home.html', {'user': request.user})


def employee_details(request):
    employee = Employee.objects.all()
    context = {
        'employee' : employee
    }
    return render(request,'employee_details.html',context)


def add_employee(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])
        new_emp = Employee(first_name=first_name, last_name=last_name,salary=salary,bonus=bonus,
                 phone=phone,dept_id=dept,role_id=role,hire_date=datetime.now())
        new_emp.save()
        return HttpResponse('Employee added successfully')
    elif request.method == 'GET':
        return render(request,'add_employee.html')
    else:
        return HttpResponse('An Exception occured! Employee not added!')

def delete_employee(request,i_id=0):
    if i_id:
        try:
            employee_to_delete = Employee.objects.get(id=i_id)
            employee_to_delete.delete()
            return HttpResponse("Employee Removed Successfully")
        except:
            return HttpResponse("Enter a Valid ID")
    employee = Employee.objects.all()
    context = {
        'employee':employee
    }
    return render(request,'delete_employee.html',context)


def filter_employee(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        employee = Employee.objects.all()
        if name:
            employee = employee.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            employee = employee.filter(dept__name__icontains = dept)
        if role:
            employee = employee.filter(role__name__icontains = role)
        context = {
            'employee' : employee
        }
        return render(request, 'employee_details.html',context)
    elif request.method == 'GET':
        return render(request,'filter_employee.html')
    else:
        return HttpResponse("An Exception Occured")


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # First, try to get the user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'User does not exist'})

        # Now, authenticate using the user's username and password
        user = authenticate(username=user.username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')# Redirect to home page after successful login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})  # Invalid password

    else:
        return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(Q(username=name) | Q(email=email)).exists():
            data = {'msg': 'User with this name or email already exists'}
            return render(request, 'signup.html', data)
        else:
            # Create user
            user1 = User.objects.create_user(username=name, email=email, password=password)
            user1.save()
            return redirect('login')  # Redirect to log in after successful signup
    else:
        return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('home')
