# Generated by Django 3.1.3 on 2021-08-21 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='user_name',
        ),
    ]