from django.db import models

class Gym (models.Model):
    name = models.CharField(max_length = 100, blank = False, null = False)
    description = models.CharField(max_length = 500, blank = True, null = True)
    location = models.CharField(max_length = 100, blank = False, null = False)
    
    class Meta:
        permissions = [
            ('can_create_gym', "can create new gym"),
            ('can_edit_gym', "can edit the gym info"),
            ('can_delete_gym', "can delete the gym"),
        ]
    
    def __str__(self): return f"{self.name} || {self.location}"