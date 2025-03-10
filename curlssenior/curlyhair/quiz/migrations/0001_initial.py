# Generated by Django 5.1.5 on 2025-01-30 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HairProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('curl_pattern', models.CharField(max_length=255)),
                ('hair_type', models.CharField(max_length=255)),
                ('vegan', models.BooleanField()),
                ('weight', models.CharField(max_length=1)),
                ('helpful_areas', models.CharField(max_length=255)),
            ],
        ),
    ]
