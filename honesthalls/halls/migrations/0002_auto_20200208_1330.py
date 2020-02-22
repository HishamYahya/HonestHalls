# Generated by Django 3.0.3 on 2020-02-08 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('halls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                 serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('anonymous', models.BooleanField()),
                ('reported', models.BooleanField()),
                ('cleanliness', models.IntegerField()),
                ('social_life', models.IntegerField()),
                ('noise', models.IntegerField()),
                ('facilities', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('contract_length', models.IntegerField()),
                ('ensuite', models.BooleanField()),
                ('basin', models.BooleanField()),
                ('bedsize', models.CharField(max_length=30)),
                ('catered', models.BooleanField()),
                ('hall',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='halls.Hall')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewPhotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('photo_path', models.CharField(max_length=100)),
                ('photo_desc', models.TextField()),
                ('review',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='halls.Review')),
                ('user',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='roomtype',
            field=models.ForeignKey(on_delete=django.
                                    db.models.deletion.CASCADE,
                                    to='halls.RoomType'),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.
                                    db.models.deletion.CASCADE,
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='HallPhotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('photo_path', models.CharField(max_length=100)),
                ('photo_desc', models.TextField()),
                ('hall',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='halls.Hall')),
            ],
        ),
    ]