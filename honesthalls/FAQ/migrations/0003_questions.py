# Generated by Django 3.0.3 on 2020-03-12 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('halls', '0002_roomtype_accessible'),
        ('FAQ', '0002_auto_20200310_2037'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(max_length=200)),
                ('answer', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='halls.Hall')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
