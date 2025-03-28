# Generated by Django 5.1.3 on 2025-02-21 15:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authorization", "0002_user_birthdate_user_tel_alter_user_third_name"),
        ("mainpage", "0002_alter_article_user_alter_subject_plan_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="class_name",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="mainpage.class",
            ),
        ),
    ]
