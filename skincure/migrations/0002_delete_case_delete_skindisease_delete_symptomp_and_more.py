# Generated by Django 4.1.3 on 2022-12-29 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("skincure", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Case",
        ),
        migrations.DeleteModel(
            name="SkinDisease",
        ),
        migrations.DeleteModel(
            name="Symptomp",
        ),
        migrations.DeleteModel(
            name="Treatment",
        ),
    ]
