# Generated by Django 3.1.7 on 2021-06-03 08:16

from django_datetime.datetime import datetime
from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store_item_stocks', '0001_initial'),
        ('wallet_models', '0004_delete_walletadjust'),
        ('staff_groups', '0001_initial'),
        ('store_item_suppliers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreItemPurchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, null=True)),
                ('request_date', models.DateField(default=datetime.dnow())),
                ('purchase_date', models.DateField(blank=True, null=True)),
                ('received_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Store Item purchases',
                'verbose_name_plural': 'Store Item purchases',
            },
        ),
        migrations.CreateModel(
            name='StoreItemPurchaseStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('price_per_unit', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=20)),
                ('is_transferred', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet_models.wallet')),
                ('item_purchase', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store_item_purchase_stock', to='store_item_purchases.storeitempurchase')),
                ('item_stock', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store_item_stocks.storeitemstock')),
                ('item_supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store_item_suppliers.storeitemsupplier')),
            ],
            options={
                'verbose_name': 'Store Item purchase stocks',
                'verbose_name_plural': 'Store Item purchase stocks',
            },
        ),
        migrations.CreateModel(
            name='StoreItemPurchaseDelivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('cost_delivery', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=20)),
                ('delivery_date', models.DateTimeField(default=datetime.dnow())),
                ('arrived_date', models.DateTimeField(blank=True, null=True)),
                ('payment_status', models.CharField(blank=True, choices=[('OPTIONAL', 'optional'), ('EXPIRED', 'expired'), ('REFUND', 'refund'), ('FAILED', 'failed'), ('UNPAID', 'unpaid'), ('PAID', 'paid')], max_length=120, null=True)),
                ('delivery_status', models.CharField(blank=True, choices=[('UNFULFILLED', 'unfulfilled'), ('DELIVERING', 'delivering'), ('RETURNING', 'returning'), ('ARRIVED', 'arrived'), ('COLLECTED', 'collected')], max_length=120, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet_models.wallet')),
                ('deliver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff_groups.staffdeliver')),
                ('item_purchase', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_purchase_deliveries', to='store_item_purchases.storeitempurchase')),
            ],
            options={
                'verbose_name': 'Store Item Purchase deliveries',
                'verbose_name_plural': 'Store Item Purchase deliveries',
            },
        ),
    ]
