from django.db import models
from django.contrib.auth.models import User
import uuid

class Meeting(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)  # Auto-add the date when created
    time = models.TimeField(auto_now_add=True)  # Auto-add the time when created
    duration = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # Duration in hours, nullable
    description = models.TextField(blank=True)  # Optional description
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)  # Meeting code, can be null
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when created
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # User who created the meeting, can be null

    def __str__(self):
        return self.title

class ChatMeeting(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Unique meeting code
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_meetings')  # The user who created/hosts the meeting
    participants = models.ManyToManyField(User, related_name='chat_meetings', blank=True)  # Participants of the meeting
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the meeting was created

    def __str__(self):
        return f"Meeting {self.code} hosted by {self.host.username}"
