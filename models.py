from django.db import models

class Message(models.Model):
    sender = models.EmailField()
    receiver = models.EmailField()
    CC = models.EmailField(blank=True)
    CCo = models.EmailField(blank=True)
    body = models.TextField()
    format = models.CharField(max_length=4)

