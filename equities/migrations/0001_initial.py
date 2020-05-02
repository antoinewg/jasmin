# Generated by Django 3.0.5 on 2020-05-02 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Greeting",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "when",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
            ],
        ),
    ]
