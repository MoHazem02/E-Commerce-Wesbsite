# Generated by Django 4.2.5 on 2023-10-07 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_alter_watchlist_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='category_items', to='auctions.category'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='auctions.bid'),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='watcher',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]