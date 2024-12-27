from django.urls import path

from employee import views

urlpatterns = [
    path('',views.home, name = 'home'),
    path('employee_details/',views.employee_details, name = 'employe_edetails'),
    path('add_employee/',views.add_employee, name = 'add_employee'),
    path('delete_employee/',views.delete_employee, name = 'delete_employee'),
    path('delete_employee/<int:emp_id>',views.delete_employee, name = 'delete_employee'),
    path('filter_employee/',views.filter_employee, name = 'filter_employee'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]