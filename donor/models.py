from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Donation(models.Model):
    donor_data = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donor_data')
    review_per_donation = models.IntegerField(null=True, blank=True)
    patient_data = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_data')
    donation_status = models.BooleanField(null=False,blank=False,default=False)
    donation_date = models.DateTimeField()
    appointment_date = models.DateTimeField(null=False,blank=False)


class Donor(models.Model):
    donor_data = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.CharField(null=False, blank=False, max_length=40, default='blank')
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    voter_id = models.CharField(null=False, blank=False, max_length=200, unique=True, default='blank')
    blood_group = models.CharField(null=False, blank=False, max_length=200)
    disease = models.BooleanField(null=False, blank=False)
    location = models.CharField(null=False, blank=False, max_length=10)
    donor_register_date = models.DateTimeField()


class UserProfile(models.Model):
    role_choice = (
        ('Patient', 'Patient'),
        ('Donor', 'Donor')
    )
    user_data = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length = 15, choices = role_choice, default = 'Patient')
