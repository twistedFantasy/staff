# Generated by Django 2.2.2 on 2019-06-24 14:44

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
            name='Assessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('status', models.CharField(choices=[('new', 'New'), ('in_progress', 'In progress'), ('failed', 'Failed'), ('completed', 'Completed')], default='in_progress', max_length=32, verbose_name='Status')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('plan', models.TextField(blank=True, null=True, verbose_name='Plan')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Comments')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('decision_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assessments_decision_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Assessments',
                'ordering': ['-id'],
            },
        ),
    ]