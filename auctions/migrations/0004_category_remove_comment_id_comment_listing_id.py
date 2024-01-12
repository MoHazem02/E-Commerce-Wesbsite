# Generated by Django 4.2.5 on 2023-09-30 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_bids_bid_rename_comments_comment_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='comment',
            name='id',
        ),
        migrations.AddField(
            model_name='comment',
            name='listing_id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
