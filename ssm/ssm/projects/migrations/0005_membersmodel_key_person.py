# Generated by Django 2.2.7 on 2019-11-22 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_project_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='membersmodel',
            name='key_person',
            field=models.BooleanField(default=False, verbose_name='Key Person'),
        ),
    ]