# Generated by Django 4.1 on 2023-09-29 03:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0002_rechargecard_assigned'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rechargecard',
            old_name='assigned',
            new_name='is_assigned',
        ),
    ]