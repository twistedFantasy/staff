# Generated by Django 2.2.7 on 2019-11-21 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_vacancy'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='task_examples',
            field=models.TextField(blank=True, null=True, verbose_name='Task Examples'),
        ),
        migrations.AddField(
            model_name='project',
            name='technology_stack',
            field=models.TextField(blank=True, null=True, verbose_name='Technology Stack'),
        ),
    ]
