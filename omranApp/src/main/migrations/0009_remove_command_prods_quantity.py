# Generated by Django 4.1.4 on 2023-03-22 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_command_prods_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='command',
            name='prods_quantity',
        ),
    ]
