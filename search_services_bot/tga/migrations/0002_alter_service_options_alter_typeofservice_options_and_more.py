# Generated by Django 4.0.3 on 2022-03-02 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tga', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'Предоставляемая услуга', 'verbose_name_plural': 'Предоставляемые услуги'},
        ),
        migrations.AlterModelOptions(
            name='typeofservice',
            options={'verbose_name': 'Тип услуги', 'verbose_name_plural': 'Тип услуги'},
        ),
        migrations.AddField(
            model_name='client',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Услуги', to='tga.service'),
        ),
        migrations.AlterField(
            model_name='client',
            name='master',
            field=models.BooleanField(verbose_name='является ли клиент мастером'),
        ),
    ]
