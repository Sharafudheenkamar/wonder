# Generated by Django 5.0.6 on 2024-06-06 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientapp', '0014_alter_assignedgroups_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wandergroup',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
