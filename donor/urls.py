from django.urls import path
from donor import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/',views.view_login, name='login'),
    path('register/', views.register, name='register'),
    path('donation_list/', views.donation_list, name='donation_list'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('review/', views.review, name='review'),
    path('logout_view/',views.logout_view, name='logout_view'),
    path('searching/',views.searching, name='searching'),
    path('donor_registration/',views.donor_registration, name='donor_registration')
]
