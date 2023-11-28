# Generated by Django 4.2.7 on 2023-11-24 18:24

from django.db import migrations, models
import rideshare.models


class Migration(migrations.Migration):
    dependencies = [
        ("rideshare", "0012_remove_passenger_picture_remove_rider_picture_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="card_detail",
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="picture",
            field=models.ImageField(
                blank=True, null=True, upload_to=rideshare.models.upload_vehicle_pic
            ),
        ),
    ]