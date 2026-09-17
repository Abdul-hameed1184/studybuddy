from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model): 
    name = models.CharField(max_length=200)
    
    def __str__(self) : 
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=200)

    host = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="hosted_rooms",
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
    )

    slug = models.SlugField(unique=True)

    description = models.TextField(
        blank=True,
        default=""
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body