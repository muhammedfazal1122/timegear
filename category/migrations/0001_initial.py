# Generated by Django 4.2.7 on 2023-12-05 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('description', models.TextField(max_length=320)),
                ('cat_image', models.ImageField(blank=True, upload_to='photos/category')),
                ('soft_deleted', models.BooleanField(default=False)),
                ('is_available', models.BooleanField(default=True)),
                ('is_offer_available', models.BooleanField(default=False)),
                ('discount', models.IntegerField(default=0)),
                ('minimum_amount', models.IntegerField(default=100)),
                ('end_date', models.DateField(null=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Category',
            },
        ),
    ]
