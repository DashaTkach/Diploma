# Generated by Django 5.0.3 on 2024-05-14 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_alter_orderitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
    ]