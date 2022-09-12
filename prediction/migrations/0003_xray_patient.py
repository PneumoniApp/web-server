# Generated by Django 4.1 on 2022-09-12 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
        ('prediction', '0002_alter_xray_img_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='xray',
            name='patient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='patient', to='patient.patient'),
            preserve_default=False,
        ),
    ]