# Generated by Django 4.2.7 on 2023-12-07 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("rideshare", "0019_alter_riderlandmark_rider_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="riderlandmark",
            name="rider",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="landmark",
                to="rideshare.rider",
            ),
        ),
    ]
