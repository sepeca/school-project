# Generated by Django 5.1.3 on 2025-02-21 15:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainpage", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="user",
            field=models.ForeignKey(
                limit_choices_to={
                    "role__in": ["teacher", "deputy director", "director"]
                },
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="subject",
            name="plan",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="subjectplancreator",
            name="creator",
            field=models.ForeignKey(
                limit_choices_to={
                    "role__in": ["teacher", "deputy director", "director"]
                },
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
