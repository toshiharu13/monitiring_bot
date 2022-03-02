# Generated by Django 4.0.3 on 2022-03-02 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tga', '0002_alter_service_options_alter_typeofservice_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Услуги', to='tga.service', verbose_name='Имя клиента'),
        ),
    ]
