# Generated by Django 4.2.7 on 2023-11-24 23:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("rideshare", "0013_delete_card_detail_alter_vehicle_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="rider",
            name="schedule",
            field=models.JSONField(
                default={
                    "schedule": {
                        "days": [0, 1, 2],
                        "end_time": "8 PM",
                        "start_time": "12 PM",
                    }
                }
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="order",
            name="passenger",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="passenger_order_status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("On Transit", "On Transit"),
                    ("Completed", "Completed"),
                ],
                default="Accepted",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="rider_order_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Accepted", "Accepted"),
                    ("Pick Up", "Pick Up"),
                    ("On Transit", "On Transit"),
                    ("Completed", "Completed"),
                ],
                max_length=10,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="trip",
            name="passengers",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="trip",
            name="rider_order_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Accepted", "Accepted"),
                    ("Pick Up", "Pick Up"),
                    ("On Transit", "On Transit"),
                    ("Completed", "Completed"),
                ],
                max_length=10,
                null=True,
            ),
        ),
        migrations.DeleteModel(
            name="passenger",
        ),
    ]
