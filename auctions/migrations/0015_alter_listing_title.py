# Generated by Django 4.2.5 on 2023-10-06 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_remove_bid_listing_remove_listing_starting_bid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='title',
            field=models.CharField(max_length=60),
        ),
    ]
