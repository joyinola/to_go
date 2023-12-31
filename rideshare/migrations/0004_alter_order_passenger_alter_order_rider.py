# Generated by Django 4.2.7 on 2023-11-17 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("rideshare", "0003_rename_order_time_order_order_datetime"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="passenger",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="rideshare.passenger"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="rider",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="rideshare.rider"
            ),
        ),
    ]
