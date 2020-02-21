from django.contrib import admin
from .models import Profile, User


class UserAdmin(admin.ModelAdmin):
    """
    The User model spec for the Django admin app.
    """

    # Show the following attributes in the corresponding table
    list_display = ('id', 'email', 'date_joined')


class ProfileAdmin(admin.ModelAdmin):
    """
    The Profile model spec for the Django admin app.
    """

    # Show the following attributes in the corresponding table
    list_display = ('id', 'user', 'verified', 'date_created')


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
