# Generated by Django 4.2.16 on 2024-10-08 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notariat', '0003_remove_recu_numero_recu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recu',
            name='date_recu',
            field=models.DateField(auto_now_add=True, verbose_name='Date de réception'),
        ),
    ]
