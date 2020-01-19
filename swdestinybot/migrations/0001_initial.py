# Generated by Django 3.0.2 on 2020-01-19 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=200)),
                ('search', models.CharField(max_length=200)),
                ('image_url', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]