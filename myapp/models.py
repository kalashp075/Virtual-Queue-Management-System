from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    birthdate = models.DateField()

    def __str__(self):
        return self.user.username
    
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)  # Optional description

    def __str__(self):
        return self.name

class QueueEntry(models.Model):
    QUEUE_CHOICES = [
        (1, 'Queue 1'),
        (2, 'Queue 2'),
        (3, 'Queue 3'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    queue_choice = models.IntegerField(choices=QUEUE_CHOICES)
    join_time = models.DateTimeField(auto_now_add=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'service')
        ordering = ['position', 'join_time']

    def __str__(self):
        return f"{self.user.username} in {self.service.name} - {self.get_queue_choice_display()}"