# Generated by Django 4.2.3 on 2023-08-03 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.CharField(default='', max_length=50),
        ),
    ]