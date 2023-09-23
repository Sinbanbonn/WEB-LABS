# Generated by Django 4.2.1 on 2023-05-23 22:35

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20)),
                ('brand', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentInvoice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('parking_number', models.IntegerField()),
                ('car_number', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('debt', models.IntegerField()),
                ('enrollment', models.IntegerField(default=0)),
                ('accrual_date', models.DateField(auto_now_add=True)),
                ('payment_date', models.DateField(auto_now=True)),
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='MyApp.car')),
            ],
        ),
        migrations.CreateModel(
            name='ParkingSpace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('price', models.IntegerField()),
                ('is_occupied', models.BooleanField(default=True)),
                ('car', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='MyApp.car')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('telephone', models.CharField(max_length=20)),
                ('date_of_birth', models.DateField()),
                ('cars', models.ManyToManyField(to='MyApp.car')),
            ],
        ),
    ]