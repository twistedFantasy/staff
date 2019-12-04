# Generated by Django 2.2.7 on 2019-11-22 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_colour'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='colour',
        ),
        migrations.AddField(
            model_name='user',
            name='color',
            field=models.CharField(blank=True, choices=[('green', 'Green'), ('yellow', 'Yellow'), ('red', 'Red'), ('black', 'Black')], max_length=32, null=True, verbose_name='Color'),
        ),
    ]