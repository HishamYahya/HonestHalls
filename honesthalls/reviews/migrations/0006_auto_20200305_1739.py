# Generated by Django 3.0.2 on 2020-03-05 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_report_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date_reported',
            field=models.DateTimeField(),
        ),
    ]