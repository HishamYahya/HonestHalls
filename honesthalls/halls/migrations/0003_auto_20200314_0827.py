# Generated by Django 3.0.3 on 2020-03-14 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('halls', '0002_roomtype_accessible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomtype',
            name='accessible',
            field=models.BooleanField(default=None, null=True),
        ),
    ]
