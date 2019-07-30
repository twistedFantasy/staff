# Generated by Django 2.2.2 on 2019-07-05 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkpoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('date', models.DateField(verbose_name='Date')),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessments.Assessment')),
            ],
            options={
                'verbose_name_plural': 'Checkpoints',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('completed', models.BooleanField(default=False, verbose_name='Completed')),
                ('checkpoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessments.Checkpoint')),
            ],
            options={
                'verbose_name_plural': 'Tasks',
                'ordering': ['-id'],
            },
        ),
    ]