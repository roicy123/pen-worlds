# Generated by Django 4.2.5 on 2024-05-15 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pens', '0009_rename_created_at_refillrequest_timestamp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='refillrequest',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
