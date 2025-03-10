# Generated by Django 4.2.7 on 2024-05-10 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clientapp", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="client",
            old_name="status",
            new_name="country",
        ),
        migrations.RemoveField(
            model_name="client",
            name="district",
        ),
        migrations.RemoveField(
            model_name="client",
            name="post",
        ),
        migrations.RemoveField(
            model_name="client",
            name="state",
        ),
        migrations.AddField(
            model_name="client",
            name="gender",
            field=models.CharField(default=True, max_length=50, null=True),
        ),
    ]
