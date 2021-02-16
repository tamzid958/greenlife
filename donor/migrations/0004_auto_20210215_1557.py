# Generated by Django 3.1.6 on 2021-02-15 09:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('donor', '0003_donor_voter_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='donor_data',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='donor_data', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='donation',
            name='patient_data',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_data', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='donor',
            name='donor_data',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=20)),
                ('user_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]