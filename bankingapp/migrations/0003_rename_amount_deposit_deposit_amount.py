# Generated by Django 4.2.7 on 2023-12-09 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bankingapp', '0002_rename_deposit_amount_deposit_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deposit',
            old_name='amount',
            new_name='deposit_amount',
        ),
    ]
