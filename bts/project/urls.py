from django.contrib import admin
from django.urls import path, include
from .views import ProjectCreationView,report,Taskstatus,AssignTaskDeleteview,TaskUpdateView,TaskDelete,TaskassignDetailView,ReportGenerateView,AssignTaskListView,AssignTaskView,ProjecttaskListView,TaskCreationView,ProjectmoduleDelete,ProjectmoduleDetailView,ProjectListView,ProjectTeamCreateView,ProjectDelete,ProjectUpdateView,ProjectmoduleCreationView,ProjectModuleListView,ProjectmoduleUpdateView,StatusCreationView
from . import views
urlpatterns = [
 
 path("create/",ProjectCreationView.as_view(),name="project_create"),
 path("list/",ProjectListView.as_view(),name="project_list"),
 path("create_team/",ProjectTeamCreateView.as_view(),name="project_team_create"),
  path("detail/<int:id>/",views.ProjectDetailView,name="project_detail"),
    path("delete/<int:pk>/",ProjectDelete.as_view(),name="project_delete"),
    path("update/<int:pk>/",ProjectUpdateView.as_view(),name="project_update"),
    path("create_module/",ProjectmoduleCreationView.as_view(),name="project_module_create"),
    path('team-members/<int:project_id>/', views.team_members_view, name='team_members'),
    path("list_module/",ProjectModuleListView.as_view(),name="project_module_list"),
    path("status_create/",StatusCreationView.as_view(),name="status_create"),
    path("module_detail/<int:pk>/", ProjectmoduleDetailView.as_view(), name="project_module_detail"),
    path("module_update/<int:pk>/",ProjectmoduleUpdateView.as_view(),name="project_module_update"),
 path("module_delete/<int:pk>/",ProjectmoduleDelete.as_view(),name="project_module_delete"),
   path("create_task/",TaskCreationView.as_view(),name="task_create"), 
   path("task_list/",ProjecttaskListView.as_view(),name="project_task_list"),
    # path('task-view/<int:project_id>/', views.TaskDetailView, name='task_view'),

  path('task-view/<int:task_id>/', views.TaskDetailView, name='task_views'),
  path('task-assign/', AssignTaskView.as_view(), name='task_assign'),
  path("task-assign-list/",AssignTaskListView.as_view(),name="task_assign_list"),

  # path("tasks_detail/<int:pk>/", TaskassignDetailView.as_view(), name="tasks_detail"),
   path("tasks_detail/<int:pk>/", TaskassignDetailView.as_view(), name="tasks_detail"),
  path("task_delete/<int:pk>/",TaskDelete.as_view(),name="task_delete"),
    path("task_update/<int:pk>/",TaskUpdateView.as_view(),name="task_update"),
      path("assign_task_delete/<int:pk>/",AssignTaskDeleteview.as_view(),name="assign_task_delete"),
      path("task_status/",views.Taskstatus.as_view(),name="taskstatus"),
      # path("report/",views.report, name="report"),
      path("reports/<int:pk>/",ReportGenerateView.as_view(),name="report"),
      
]
