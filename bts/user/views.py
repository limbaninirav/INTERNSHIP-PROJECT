from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import User
from .forms import ManagerCreationForm,DeveloperCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
#import Setting .py
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.generic import ListView
from project.models import Project
from django.shortcuts import redirect,reverse
from project.models import UserTask,Task,Status,ProjectModule
from project.forms import TaskAsignForm,StatusCreationForm,TaskCreationForm
from django.views import View




# Create your views here.

class ManagerRegisterView(CreateView):
    model = User
    form_class = ManagerCreationForm
    template_name = 'user/manager_register.html'
    success_url = reverse_lazy('login')
 
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        # print("email.....",email)
        if sendMail(email):
            print("mail sent")
            return super().form_valid(form)
        else:
            return super().form_valid(form)


class DeveloperRegisterView(CreateView):
    model = User
    form_class = DeveloperCreationForm
    template_name = 'user/developer_register.html'
    success_url = '/login/'   

class UserLoginView(LoginView):  
    template_name = 'user/login.html' 
    model = User  
    
    def get_redirect_url(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_manager:
                return '/user/manager_dashboard/'
            else:
                return '/user/developer_dashboard/'

class UserLogoutView(LogoutView):
    model = User
    def get_redirect_url(self):
        if not(self.request.user.is_authenticated):
            return '/user/login/'
    

def sendMail(to):
    subject ='Welcome To Project'
    message = 'Hope you are enjoying'
    recipentList = [to]
    # recipentList = ["exocon789@gmail.com"]
    EMAIL_FROM = settings.EMAIL_HOST_USER
    send_mail(subject, message, EMAIL_FROM, recipentList)
    return HttpResponse('email sent')
    return True


class ManagerDashboardview(ListView):




      def get(self, request, *args, **kwargs):
        #logic to get all the projects
        
        projects = Project.objects.all() #select * from project
        project_count = Project.objects.count()
        module_count = ProjectModule.objects.count()
        task_count = Task.objects.count()
        developer_count = UserTask.objects.values('user').distinct().count()
        user_tasks = UserTask.objects.all()
        
        return render(request, 'user/manager_dashboard.html',{
            "projects":projects,
            'project_count':project_count,
            'module_count': module_count,
            'task_count': task_count,
            'developer_count': developer_count,
            'user_tasks':user_tasks,
        })
    
    
        template_name = 'user/manager_dashboard.html'

        

      

class DevloperDashboardView(ListView):
    model = UserTask

    def get_queryset(self, **kwargs):
        tasks = UserTask.objects.filter(user=self.request.user)
        tasks_in_progress = tasks.filter(task__status='In Progress')
        tasks_testing = tasks.filter(task__status='Testing')
        tasks_not_started = tasks.filter(task__status='Not Started')
        
        return tasks_in_progress.union(tasks_testing, tasks_not_started)
 
    template_name = 'user/developer_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Count of tasks in each category
        context['tasks_in_progress_count'] = UserTask.objects.filter(user=self.request.user, task__status='In Progress').count()
        context['tasks_testing_count'] = UserTask.objects.filter(user=self.request.user, task__status='Testing').count()
        context['tasks_not_started_count'] = UserTask.objects.filter(user=self.request.user, task__status='Not Started').count()

        return context



# class StatusUpdateView(UpdateView):
#      model = UserTask
#      form_class = TaskAsignForm
#      success_url = "/user/developer_dashboard/"
#      template_name = "user/status_update.html" 


# class StatusUpdateViews(UpdateView):
#      model = Status
#      form_class = StatusCreationForm
#      success_url = "/user/developer_dashboard/"
#      template_name = "user/status_update.html"  

from django.shortcuts import redirect
from django.urls import reverse
from project.models import Task
from django.utils import timezone
class StatusUpdateView(View):
    def post(self, request, pk):
        task = Task.objects.get(id=pk)
        if task.status == 'Not Started':
            task.status = 'In Progress'
        elif task.status == 'In Progress':
            task.status = 'Testing'
        task.updated_at = timezone.now()  # Update the 'updated_at' field with the current timestamp
        task.save()

        return redirect(reverse('Developer_dashboard'))




 
    