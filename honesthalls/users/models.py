from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Represents a HonestHalls user profile.
    Contains data complementing that of django.contrib.auth.models.User
    """

    # Reference to the user model which holds
    # email, username, names & password.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # TODO: Implement user verification.
    verified = models.BooleanField(default=False)

    # Automatically set to the right date & time.
    date_created = models.DateTimeField(auto_now_add=True)

    @receiver(post_save, sender=User)
    def on_user_saved(sender, instance, created, **kwargs):
        """
        Called whenever the User model is saved or created.
        Saves/creates the corresponding Profile.
        """
        if created:
            Profile.objects.create(user=instance)
        else:
            instance.profile.save()
