# Generated by Django 3.0.2 on 2020-03-05 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='review',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='reviews.Review'),
            preserve_default=False,
        ),
    ]