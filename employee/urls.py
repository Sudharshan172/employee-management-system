from django.urls import path

from employee import views

urlpatterns = [
    path('',views.home, name = 'home'),
    path('employee_details/',views.employee_details, name = 'employeedetails'),
    path('add_employee/',views.add_employee, name = 'addemployee'),
    path('delete_employee/',views.delete_employee, name = 'deleteemployee'),
    path('delete_employee/<int:i_id>',views.delete_employee, name = 'deleteemployee'),
    path('filter_employee/',views.filter_employee, name = 'filteremployee'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]