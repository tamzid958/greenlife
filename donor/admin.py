# Register your models here.
from django.contrib import admin
from donor.models import UserProfile, Donor, Donation

admin.site.register(UserProfile)
admin.site.register(Donor)
admin.site.register(Donation)
