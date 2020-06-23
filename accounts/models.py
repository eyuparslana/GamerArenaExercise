from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_info')
    website = models.CharField(max_length=255)
    bio = models.TextField(max_length=1000)
    location = models.CharField(max_length=55)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.user_info.save()
