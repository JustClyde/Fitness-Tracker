# Generated by Django 4.2.2 on 2023-06-23 02:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracker", "0005_person_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="maintainance",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
