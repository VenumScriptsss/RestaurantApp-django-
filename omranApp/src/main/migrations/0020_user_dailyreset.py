# Generated by Django 4.1.7 on 2023-04-19 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_user_admin_user_tablesnum'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='dailyReset',
            field=models.BooleanField(default=False),
        ),
    ]
