# Generated by Django 4.2.7 on 2023-11-17 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("rideshare", "0005_order_reference"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="passenger",
            name="card",
        ),
        migrations.AddField(
            model_name="order",
            name="rider_order_status",
            field=models.CharField(
                choices=[("Accepted", "Accepted"), ("Declined", "Declined")],
                default="Accepted",
                max_length=10,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="trip",
            name="passengers",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="rideshare.passenger",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="passenger",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="rideshare.passenger",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="passenger_order_status",
            field=models.CharField(
                choices=[
                    ("Accepted", "Accepted"),
                    ("On Transit", "On Transit"),
                    ("Completed", "Completed"),
                    ("Cancelled", "Cancelled"),
                ],
                default="Accepted",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="trip",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order",
                to="rideshare.trip",
            ),
        ),
    ]
