# Generated by Django 5.0 on 2023-12-13 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0018_delete_dates_alter_lesson_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='date',
            field=models.DateField(),
        ),
    ]
