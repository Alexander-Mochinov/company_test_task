# Generated by Django 3.2.7 on 2022-01-29 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drf_api', '0011_auto_20220129_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departmentclientref',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_departament', to='drf_api.department', unique=True, verbose_name='департамент'),
        ),
        migrations.AlterField(
            model_name='departmentlegalentityref',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='drf_api.department', unique=True, verbose_name='департамент'),
        ),
    ]
