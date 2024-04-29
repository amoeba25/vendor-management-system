# Generated by Django 4.2.11 on 2024-04-27 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendorapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='average_response_time',
            field=models.FloatField(blank=True, help_text='Average time taken to acknowledge purchase orders', null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='fullfillment_rate',
            field=models.FloatField(blank=True, help_text='Percentage of orders that are fullfilled succesfully', null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='on_time_delivery_rate',
            field=models.FloatField(blank=True, help_text='Percentage of on-time deliveries', null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='quality_rating_avg',
            field=models.FloatField(blank=True, help_text='Average rating of quality based on product purchase', null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vendor_code',
            field=models.CharField(blank=True, help_text='Unique vendor code', max_length=10, unique=True),
        ),
    ]
