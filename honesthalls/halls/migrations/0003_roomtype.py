# Generated by Django 3.0.3 on 2020-02-04 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('halls', '0002_hallphotos'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('contract_length', models.IntegerField()),
                ('ensuite', models.BooleanField()),
                ('basin', models.BooleanField()),
                ('bedsize', models.CharField(max_length=30)),
                ('catered', models.BooleanField()),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='halls.Hall')),
            ],
        ),
    ]