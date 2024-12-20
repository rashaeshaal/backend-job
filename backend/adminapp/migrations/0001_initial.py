# Generated by Django 5.0.3 on 2024-12-06 07:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('industry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='adminapp.industry')),
            ],
        ),
        migrations.CreateModel(
            name='JobPosting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=255)),
                ('job_description', models.TextField()),
                ('salary_min', models.DecimalField(decimal_places=2, max_digits=10)),
                ('salary_max', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('job_industry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.industry')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_jobs', to=settings.AUTH_USER_MODEL)),
                ('job_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.role')),
            ],
        ),
    ]
