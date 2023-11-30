# Generated by Django 4.2.7 on 2023-11-27 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("rideshare", "0014_rider_schedule_alter_order_passenger_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="accountdetail",
            old_name="back_code",
            new_name="bank_code",
        ),
        migrations.RenameField(
            model_name="rider",
            old_name="price",
            new_name="rider_price",
        ),
        migrations.RemoveField(
            model_name="accountdetail",
            name="account_type",
        ),
        migrations.RemoveField(
            model_name="accountdetail",
            name="currency",
        ),
        migrations.RemoveField(
            model_name="trip",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="trip",
            name="passengers",
        ),
        migrations.AddField(
            model_name="order",
            name="rider_pay_ref",
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="trip",
            name="amount_raised",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="trip",
            name="started_at",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="order_datetime",
            field=models.DateTimeField(blank=True, null=True),
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
                default="Pending",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="trip",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="trip",
                to="rideshare.trip",
            ),
        ),
        migrations.AlterField(
            model_name="rider",
            name="vehicle",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="rider",
                to="rideshare.vehicle",
            ),
        ),
        migrations.AlterField(
            model_name="trip",
            name="rider",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="rideshare.rider"
            ),
        ),
        migrations.AlterField(
            model_name="trip",
            name="rider_order_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Pick Up", "Pick Up"),
                    ("On Transit", "On Transit"),
                    ("Completed", "Completed"),
                ],
                max_length=10,
                null=True,
            ),
        ),
        migrations.CreateModel(
            name="RiderLandmark",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("route_to", models.CharField(max_length=255)),
                ("rider_price", models.CharField(max_length=50)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "rider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="rideshare.rider",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="order",
            name="landmark",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="rideshare.riderlandmark",
            ),
        ),
    ]
