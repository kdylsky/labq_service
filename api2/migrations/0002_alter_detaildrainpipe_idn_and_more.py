# Generated by Django 4.1.3 on 2022-11-09 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api2", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="detaildrainpipe",
            name="idn",
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name="detailrainfall",
            name="raingauge_code",
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name="drainpipe",
            name="gubn",
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name="drainpipe",
            name="gubn_nam",
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name="rainfall",
            name="gu_code",
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name="rainfall",
            name="gu_name",
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
