# Generated by Django 3.0.3 on 2020-03-16 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FAQ', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='answer',
            field=models.TextField(blank=True),
        ),
    ]
