# Generated by Django 3.2.7 on 2022-01-29 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drf_api', '0012_auto_20220129_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departmentclientref',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='drf_api.client', unique=True, verbose_name='Физ лицо'),
        ),
        migrations.AlterField(
            model_name='departmentclientref',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_departament', to='drf_api.department', verbose_name='департамент'),
        ),
        migrations.AlterField(
            model_name='departmentlegalentityref',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='drf_api.department', verbose_name='департамент'),
        ),
        migrations.AlterField(
            model_name='departmentlegalentityref',
            name='legal_entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='drf_api.legalentity', unique=True, verbose_name='Юр. лицо'),
        ),
    ]