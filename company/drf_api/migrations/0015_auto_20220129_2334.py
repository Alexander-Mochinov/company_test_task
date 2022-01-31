# Generated by Django 3.2.7 on 2022-01-29 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drf_api', '0014_auto_20220129_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='departments',
            field=models.ManyToManyField(through='drf_api.DepartmentClientRef', to='drf_api.Department', verbose_name='Департаменты'),
        ),
        migrations.AlterField(
            model_name='departmentclientref',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_departament', to='drf_api.department', verbose_name='Департамент'),
        ),
        migrations.AlterField(
            model_name='departmentlegalentityref',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entity_departament', to='drf_api.department', verbose_name='департамент'),
        ),
        migrations.AlterField(
            model_name='legalentity',
            name='departments',
            field=models.ManyToManyField(through='drf_api.DepartmentLegalEntityRef', to='drf_api.Department', verbose_name='Департаменты'),
        ),
    ]