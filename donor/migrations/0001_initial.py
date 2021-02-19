# Generated by Django 3.1.6 on 2021-02-19 16:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Patient', 'Patient'), ('Donor', 'Donor')], default='Patient', max_length=15)),
                ('user_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.CharField(default='blank', max_length=40)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('voter_id', models.CharField(default='blank', max_length=200, unique=True)),
                ('blood_group', models.CharField(max_length=200)),
                ('disease', models.BooleanField()),
                ('location', models.CharField(max_length=10)),
                ('donor_register_date', models.DateTimeField()),
                ('donor_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_per_donation', models.IntegerField(blank=True, null=True)),
                ('donation_status', models.BooleanField(default=False)),
                ('donation_date', models.DateTimeField()),
                ('appointment_date', models.DateTimeField()),
                ('donor_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donor_data', to=settings.AUTH_USER_MODEL)),
                ('patient_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_data', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
