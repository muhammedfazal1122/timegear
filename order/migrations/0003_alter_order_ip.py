# Generated by Django 4.2.7 on 2024-06-06 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_order_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ip',
            field=models.CharField(default='127.0.0.1', max_length=20, null=True),
        ),
    ]