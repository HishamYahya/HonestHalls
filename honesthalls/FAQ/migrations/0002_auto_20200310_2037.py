# Generated by Django 3.0.2 on 2020-03-10 20:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('halls', '0002_roomtype_accessible'),
        ('FAQ', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='QuestionAnswer',
            new_name='Questions',
        ),
    ]
