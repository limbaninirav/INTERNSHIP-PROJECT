from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from .forms import ProjectCreationForm,ProjectModuleCreationForm,StatusCreationForm,TaskCreationForm,TaskAsignForm
from .models import Project,ProjectTeam,Task,UserTask,Status
from .forms import ProjectTeamCreationForm,StatusCreationForm
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import User,ProjectModule,Status
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings

from django.http import FileResponse
import io
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import inch
# from reportlab.lib.pagesizes import letter








def report(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    tasks = UserTask.objects.filter(user=request.user)
    
    for task in tasks:
        textob.textLine(f'Task Name: {task.task.task_name}')
        textob.textLine(f'Assigned To: {task.user.username}')
        textob.textLine(f'Status: {task.task.status}')
        textob.textLine(f'Created At: {task.created_at}')
        textob.textLine(f'Last Updated At: {task.updated_at}')
        textob.textLine('--------------------------------------')

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='report.pdf')

# Create your views here.

class ProjectCreationView(CreateView):
    template_name = 'project/create.html'
    model = Project
    form_class = ProjectCreationForm
    success_url = '/project/list/'
    
    

class ProjectListView(ListView):
    template_name = 'project/list.html'
    model = Project
    context_object_name = 'projects'


class ProjectTeamCreateView(CreateView):    
    template_name = 'project/create_team.html'
    model = ProjectTeam
    success_url = '/project/list/'
    form_class = ProjectTeamCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter users to only include developers
        developers = User.objects.filter(is_developer=True)
        context['form'].fields['user'].queryset = developers
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        project_id = self.request.GET.get('project_id')
        if project_id:
            project = get_object_or_404(Project, id=project_id)
            kwargs['initial']['project'] = project
        return kwargs
    
    def manager_users_view(request):
        manager_users = User.objects.filter(role='is_manager')
        return render(request, 'project/manager_users.html', {'manager_users': manager_users})
    

    
    
# def TeamDetailView(request,id):
#     contect = {}
#     project = Project.objects.get(id=id)
#     contect["project"] = project
    
#     return render(request,"project/team_detail.html",contect)

                                                                                                                                  
class ProjectmoduleCreationView(CreateView):
    template_name = 'project/create_module.html'
    model = ProjectModule
    form_class = ProjectModuleCreationForm
    success_url = '/project/list_module/'

    def dispatch(self, request, *args, **kwargs):
        # Get the project ID from the URL query parameter
        project_id = self.request.GET.get('project_id')
        
        # If a project ID is provided, retrieve the project object
        if project_id:
            try:
                project = ProjectModule.objects.get(id=project_id)
                
                # Set the initial data for the form based on the retrieved project
                self.form_class.initial['project'] = project
                self.form_class.initial['status'] = project.status
                self.form_class.initial['module_type'] = project.moduleName
            
            except ObjectDoesNotExist:
                pass
        
        return super().dispatch(request, *args, **kwargs)
    

def task_view(request, project_id):
    project = Task.objects.prefetch_related('user').filter(project_id=project_id)
    
    task_view = []
    for item in project:
        user = get_object_or_404(Task, id=item.user_id)
        task_view.append({
            'id': item.user_id,
            'username': user.module,
            # Other relevant information
        })
        
    return render(request, 'task/task_view.html', {'task_view': task_view})
    
class ProjectmoduleDetailView(DetailView):
    model = ProjectModule
    context_object_name = "ProjectModule"
    template_name = "project/project_module_detail.html" 

# def ProjectmoduleDetailView(request,id):
#     contect = {}
#     project = ProjectModule.objects.get(id=id)
#     contect["ProjectModule"] = project
    
#     return render(request,"project/project_module_detail.html",contect)

class ProjectmoduleUpdateView(UpdateView):
     model = ProjectModule
     form_class = ProjectModuleCreationForm
     success_url = "/project/list_module/"
     template_name = "project/project_module_update.html"   

class ProjectmoduleDelete(DeleteView):
     model = ProjectModule
     template_name = "project/project_module_delete.html"    
     success_url = "/project/list_module/"

 
    
class ProjectModuleListView(ListView):
    template_name = 'project/list_module.html'
    model = ProjectModule
    context_object_name = 'projectmodules'  

class StatusCreationView(CreateView):
    template_name = 'project/status.html'
    model = Status
    form_class = StatusCreationForm
    success_url = '/project/list/'
    
#crud operatins
# class ProjectDetailView(DetailView):
#     model = Project
#     context_object_name = "Project"
#     template_name = "project/project_detail.html"
    
# class TeamMembersListView(ListView):
#     model = Project
#     context_object_name = "project"
#     template_name = "yourapp/teammember_list.html"    
    
# def team_members_view(request, project_id):
#     project = ProjectTeam.objects.prefetch_related('user').filter(project_id=project_id)
#     team_members = list(project.values_list('user', flat=True))
#     return render(request, 'project/team_member.html', {'team_members': team_members})
    

def team_members_view(request, project_id):
    project = ProjectTeam.objects.prefetch_related('user').filter(project_id=project_id)
    
    team_members = []
    for item in project:
        user = get_object_or_404(User, id=item.user_id)
        team_members.append({
            'id': item.user_id,
            'username': user.username,
            # Other relevant information
        })
        
    return render(request, 'project/team_member.html', {'team_members': team_members})



def ProjectDetailView(request,id):
    contect = {}
    project = Project.objects.get(id=id)
    contect["project"] = project
    
    return render(request,"project/project_detail.html",contect)

class ProjectDelete(DeleteView):
     model = Project
     template_name = "project/project_delete.html"    
     success_url = "/project/list/"

class ProjectUpdateView(UpdateView):
     model = Project
     form_class = ProjectCreationForm
     success_url = "/project/list/"
     template_name = "project/project_update.html"    


class TaskCreationView(CreateView):
    template_name = 'task/create_task.html'
    model = Task
    form_class = TaskCreationForm
    success_url = '/project/task_list/'

    

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['projectmodules'] = self.request.GET.get('projectmodules', None)
    #     return context
    
class ProjecttaskListView(ListView):
    template_name = 'task/list.html'
    model = Task
    context_object_name = 'tasks'


def TaskDetailView(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task/task_detail.html', {'task': task})


class AssignTaskView(CreateView):
    model = UserTask
    template_name = 'project/assign_task.html'
    success_url = '/project/task-assign-list/'
    form_class = TaskAsignForm
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter users to only include developers
        developers = User.objects.filter(is_developer=True)
        context['form'].fields['user'].queryset = developers
        return context
    
    def form_valid(self, form):
        task = form.save(commit=False)
        task.developer = self.request.user  # Assign the task to the current user (developer)
        task.save()

        # Get the task details
        task_details = f"Task Name: {task.task.task_name}\nDescription: {task.task.description}\nPriority: {task.task.priority}\nTotal Minutes: {task.task.totalMinutes}"

        # Send email to developer with task details
        send_mail(
            'Task Assigned',
            task_details,
            settings.EMAIL_HOST_USER,
            [self.request.user.email],
            fail_silently=False,
        )

        return super().form_valid(form)

# def sendMail(to):
#     subject = 'Welcome to BTS'
#     message = 'Hope you are enjoying your Django Tutorials'
#     #recepientList = ["samir.vithlani83955@gmail.com"]
#     recepientList = [to]
#     EMAIL_FROM = settings.EMAIL_HOST_USER
#     send_mail(subject,message, EMAIL_FROM, recepientList)
#     #attach file
#     #html
#     return True

class AssignTaskListView(ListView):
    template_name = 'project/assign_task_list.html'
    model = UserTask
    context_object_name = 'usertasks'

class TaskassignDetailView(DetailView):
    model = Task
    context_object_name = "Tasks"
    template_name = "project/taskassigndetailview.html" 

class TaskDelete(DeleteView):
     model = Task
     template_name = "task/task_delete.html"    
     success_url = "/project/task_list/"

class TaskUpdateView(UpdateView):
     model = Task
     form_class = TaskCreationForm
     success_url = "/project/task_list/"
     template_name = "task/task_update.html"  

class AssignTaskDeleteview(DeleteView):
     model = UserTask
     template_name = "task/task_delete.html"    
     success_url = "/project/task-assign-list/"


def sendMail(to):
    subject ='Welcome To BTS24'
    message = 'Hope you are enjoying'
    recipentList = [to]
    # recipentList = ["exocon789@gmail.com"]
    EMAIL_FROM = settings.EMAIL_HOST_USER
    send_mail(subject, message, EMAIL_FROM, recipentList)
    return HttpResponse('email sent')
    return True


class Taskstatus(ListView):
    model = UserTask

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = UserTask.objects.filter(user=self.request.user)
        tasks_in_progress = tasks.filter(task__status='In Progress')
        tasks_testing = tasks.filter(task__status='Testing')
        tasks_not_started = tasks.filter(task__status='Not Started')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context
        return context
 
    template_name = 'project/task_status.html'


class ReportGenerateView(ListView):
 
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')

        project = get_object_or_404(Project, pk=pk)
        module = ProjectModule.objects.filter(project=project)
        task = Task.objects.filter(project=project)
        developer = ProjectTeam.objects.filter(project=project)
        
        tasks = []
        total_hours = 0
        total_minutes = 0        
        
        for item in task:
            
            time_difference = item.updated_at - item.created_at
            
            hours = int(time_difference.total_seconds() // 3600)
            minutes = int((time_difference.total_seconds() % 3600) // 60)
            
            total_hours += hours
            total_minutes += minutes
            
            if UserTask.objects.filter(task_id=item.id).exists():
                usertask = UserTask.objects.get(task_id=item.id)
                user = User.objects.get(pk=usertask.user_id)
            else: 
                user = ''
            
            tasks.append({
                'task_name': item.task_name,
                'description': item.description,
                'status_name': item.status,
                'totalMinutes': item.totalMinutes,
                'user': user,
                'hours' : hours,
                'minutes' : minutes
            })
        
        # Convert excess minutes to hours
        total_hours += total_minutes // 60
        total_minutes %= 60
            
        
        return render(request,"project/report.html",{
            'project':project,
            'module':module,
            'task':tasks,
            'developer':developer,
            'pagename':'Report',
            'total_hours':total_hours,
            'total_minutes':total_minutes,
        })