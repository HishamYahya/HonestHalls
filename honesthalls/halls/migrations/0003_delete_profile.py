# Generated by Django 2.2.7 on 2020-02-05 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('halls', '0002_profile_verified'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]