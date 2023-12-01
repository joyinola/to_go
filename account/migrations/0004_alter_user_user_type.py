# Generated by Django 4.2.7 on 2023-11-24 23:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0003_user_user_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                choices=[("rider", "rider"), ("passenger", "passenger")],
                default="passenger",
                max_length=10,
            ),
        ),
    ]
