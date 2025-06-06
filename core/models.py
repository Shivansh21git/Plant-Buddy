from django.db import models
from django.contrib.auth.models import User


# defining the model here 
class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    device_id = models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateField(auto_now_add=True)


    def __self__(self):
        return f"{self.name} ({self.device_id})"