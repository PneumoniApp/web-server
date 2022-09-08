# Generated by Django 4.1 on 2022-09-08 22:32

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
            name='XRay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('img', models.ImageField(upload_to='xray_images/')),
                ('result', models.BooleanField(default=0)),
                ('normal_level', models.FloatField(default=0.0)),
                ('pneumonia_level', models.FloatField(default=0.0)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='xray', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
