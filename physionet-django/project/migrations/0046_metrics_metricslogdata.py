# Generated by Django 2.2.13 on 2020-08-17 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0045_auto_20200805_1001'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetricsLogData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=128)),
                ('creation_datetime', models.DateTimeField()),
                ('log_hash', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Metrics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewcount', models.PositiveIntegerField(default=0)),
                ('running_viewcount', models.PositiveIntegerField(default=0)),
                ('date', models.DateField()),
                ('core_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.CoreProject')),
            ],
            options={
                'unique_together': {('core_project', 'date')},
            },
        ),
    ]
