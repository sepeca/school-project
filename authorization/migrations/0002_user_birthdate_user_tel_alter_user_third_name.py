# Generated by Django 5.1.3 on 2025-02-20 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authorization", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="birthdate",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="tel",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="third_name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
