# Generated by Django 4.2.2 on 2023-06-25 03:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracker", "0007_exercise_type_food_calories_food_date_food_meal_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="exercise",
            name="calories",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="exercise",
            name="date",
            field=models.DateTimeField(default=datetime.date(2023, 6, 25)),
        ),
        migrations.AlterField(
            model_name="food",
            name="date",
            field=models.DateTimeField(default=datetime.date(2023, 6, 25)),
        ),
    ]
