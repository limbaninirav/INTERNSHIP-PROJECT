from django.db import models
from user.models import User
from django.core.exceptions import ValidationError

def validate_date_format(value):
    # Add your date validation logic here
    if not value:  # Example validation, adjust as needed
        raise ValidationError("Date cannot be empty")


# Create your models here.
techChoices = (
("Python", "Python")
, ("Java","Java"),
("C++", "C++"),
)
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(choices=techChoices, max_length=100)
    estimated_hours = models.PositiveIntegerField()
    StartDate = models.DateField()
    endDate = models.DateField()
                                  
    class Meta:
       db_table = "project"   

    def __str__(self):
        return self.name

class ProjectTeam(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
       db_table = "projectteam"  

    def __str__(self):
         return self.user.username
       
statusChoices = (
("In Progress", "In Progress"), 
("Not Started","Not Started"),
("Testing", "Testing"),
)
class Status(models.Model):
        status_name= models.CharField(choices=statusChoices, max_length=100)

        class Meta:
            db_table = "Status"   

        def __str__(self)  -> str:
         return self.status_name    

class ProjectModule(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    moduleName = models.CharField(max_length=100)
    description = models.TextField()
    estimatedhours = models.PositiveIntegerField()
    status = models.CharField(choices=statusChoices,max_length=100)
    startDate = models.DateField()
   

    class Meta:
            db_table = "project_module"  

    def __str__(self)  -> str:
         return self.moduleName
priorotyChoices = (
("High", "High"), 
("Low","Low"),

)
class Task(models.Model):
        module = models.ForeignKey(ProjectModule, on_delete=models.CASCADE)
        project = models.ForeignKey(Project, on_delete=models.CASCADE)
        status = models.CharField(default='Not Started', max_length=100, choices=statusChoices)
        task_name = models.CharField(max_length=100)
        priority = models.CharField(choices=priorotyChoices , max_length=100)
        description = models.TextField()
        totalMinutes = models.PositiveIntegerField()
        created_at= models.DateTimeField(auto_now_add=True, null = True, blank=True)
        updated_at= models.DateTimeField(auto_now_add=True, null = True, blank=True)

        class Meta:
            db_table = "task"

        def __str__(self):
             return self.task_name

        

class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True, null = True, blank=True)
    updated_at= models.DateTimeField(auto_now_add=True, null = True, blank=True)

    class Meta:
        db_table = "user_task"

    

    
                                    

