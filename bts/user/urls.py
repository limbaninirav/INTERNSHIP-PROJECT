from django.contrib import admin
from django.urls import path,include
from .views import ManagerRegisterView,DeveloperRegisterView,UserLoginView,UserLogoutView,ManagerDashboardview,DevloperDashboardView,StatusUpdateView
from django.contrib.auth.views import LogoutView
from. import views




urlpatterns = [

#localhost:8000/user/manager_register/
path("manager_register/",ManagerRegisterView.as_view(),name="manager_register"),
path("developer_register/",DeveloperRegisterView.as_view(),name="developer_register"),
path('login/', UserLoginView.as_view(), name='login'),
path("logout/", UserLogoutView.as_view(next_page = "/user/login"), name="logout"),
path("sendmail/", views.sendMail, name="sendmail"),
path("manager_dashboard/",views.ManagerDashboardview.as_view(),name="manager_dashboard"),
path("developer_dashboard/",views.DevloperDashboardView.as_view(),name="Developer_dashboard"),
 path("task_update/<int:pk>/",views.StatusUpdateView.as_view(),name="Status_update"),




] 