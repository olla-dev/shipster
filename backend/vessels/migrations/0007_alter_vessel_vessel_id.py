# Generated by Django 4.1.1 on 2022-10-02 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vessels', '0006_alter_location_id_alter_vessel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vessel',
            name='vessel_id',
            field=models.BigIntegerField(blank=True, null=True, unique=True),
        ),
    ]
