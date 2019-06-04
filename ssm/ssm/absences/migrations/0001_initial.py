# Generated by Django 2.2.1 on 2019-06-03 12:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('reason', models.CharField(choices=[('vacation', 'Vacation'), ('illness', 'Illness'), ('holiday', 'Holiday'), ('other', 'Other')], default='other', max_length=32, verbose_name='Reason')),
                ('status', models.CharField(choices=[('new', 'New'), ('veryfing', 'Verifying'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='new', max_length=32, verbose_name='Status')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='absences_approved_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Absences',
                'ordering': ['-id'],
            },
        ),
    ]
