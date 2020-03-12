from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    """
    Define a model manager for our custom User model.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """ Creates a new User and saves it to the database. """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """ Creates a new User and saves it to the database. """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """ Creates a new *superuser* User and saves it to the database. """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Users within the authentication system are represented by this
    model.

    Email and password are required. Other fields are optional.
    """

    username = None
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'

    # email is automatically addded to REQUIRED_FIELDS due
    # to being used as USERNAME_FIELD.
    REQUIRED_FIELDS = []

    # Set our custom UserManager.
    objects = UserManager()

    @property
    def first_name_initial(self):
        return self.first_name and self.first_name[0]

    @property
    def last_name_initial(self):
        return self.last_name and self.last_name[0]

    def __str__(self):
        prefix = ('[SU] ' if self.is_superuser else
                  '[STAFF] ' if self.is_staff else
                  ' ')
        return f'{prefix}{self.email}'


class Profile(models.Model):
    """
    Represents a HonestHalls user profile.
    Contains data complementing that of the User model.
    """

    # Reference to the user model which holds
    # email, username, names & password.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # TODO: Implement user verification.
    verified = models.BooleanField(default=False)

    @property
    def date_created(self):
        return self.user.date_joined

    def __str__(self):
        return f'{self.user}, Verified: {self.verified}'

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
