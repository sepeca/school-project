# Generated by Django 5.1.3 on 2025-03-07 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authorization", "0004_user_avatar"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="about_me",
            field=models.TextField(blank=True, null=True),
        ),
    ]
