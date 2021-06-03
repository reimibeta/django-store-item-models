# Generated by Django 3.1.7 on 2021-06-03 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store_items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreItemStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('is_available', models.BooleanField(default=True)),
                ('item', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_stock', to='store_items.storeitem')),
            ],
            options={
                'unique_together': {('id', 'item')},
            },
        ),
    ]