# Generated by Django 3.2.6 on 2021-08-13 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0004_auto_20210811_1245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='state',
            new_name='country',
        ),
    ]
