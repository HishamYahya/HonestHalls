# Generated by Django 3.0.2 on 2020-02-13 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('halls', '0002_auto_20200208_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hallphotos',
            name='photo_path',
            field=models.ImageField(upload_to='uploads/'),
        ),
    ]