# Generated by Django 4.0.4 on 2022-05-04 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_remove_prescriptions_pet_pet_prescriptions'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Prescriptions',
            new_name='Prescription',
        ),
    ]
