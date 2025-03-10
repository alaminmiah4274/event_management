from django.db import models
from django.contrib.auth.models import AbstractUser
from tasks.models import Event


# Create your models here.
class CustomUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to="profile_images", blank=True, default="profile_images/anonymous.jpg"
    )
    phone_number = models.CharField(max_length=11, unique=True, blank=True, null=True)
    event = models.ManyToManyField(Event, related_name="participant")

    def __str__(self):
        return self.username
