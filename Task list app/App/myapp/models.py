from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=111)  
    description = models.TextField()  
    status = models.CharField(max_length=33)  
    due_date = models.DateTimeField(verbose_name="Deadline")  

    def __str__(self):
        return self.title
