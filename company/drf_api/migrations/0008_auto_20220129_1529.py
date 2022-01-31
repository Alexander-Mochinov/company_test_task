# Generated by Django 3.2.7 on 2022-01-29 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drf_api', '0007_auto_20220129_1525'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='socialnetworks',
            options={'verbose_name': 'Социальная сеть', 'verbose_name_plural': 'Социальные сети'},
        ),
        migrations.AlterField(
            model_name='socialnetworksref',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='drf_api.client', verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='socialnetworksref',
            name='social_networks',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='drf_api.socialnetworks', verbose_name='Соц. сеть'),
        ),
        migrations.AlterModelTable(
            name='socialnetworks',
            table='social_networks',
        ),
    ]
