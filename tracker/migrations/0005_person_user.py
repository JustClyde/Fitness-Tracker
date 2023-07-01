# Generated by Django 4.2.2 on 2023-06-23 01:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tracker", "0004_remove_person_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="user",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_person",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
