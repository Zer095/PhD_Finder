from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from positions.models import Position
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.
class CustomUser(AbstractUser):

    # Add a field to store the saved position
    saved = ArrayField(models.IntegerField(), null=True)

    # Save the position
    def save_pos(self, id):
        if Position.objects.filter(id=id).exists():
            self.saved.append(id)
            return True
        else:
            return False

    def __str__(self):
        return self.username
    

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    saved = ArrayField(models.IntegerField(), default=list)

    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=CustomUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    