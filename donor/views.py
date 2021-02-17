import os
from datetime import datetime
from pathlib import Path
import cv2
import pytesseract
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from donor.models import UserProfile as Role, Donor, UserProfile, Donation
from django.db.models import Sum
# Create your views here.

BASE_DIR = Path(__file__).resolve().parent.parent


def home(request):
    context = {
        'page_title': 'Home',
        'nbar': 'index',
        'donor_list': Donor.objects.all()[:10]
    }
    return render(request, 'index.html', context)


def view_login(request):
    if request.method == 'POST':
        username = request.POST['User']
        password = request.POST['Password']
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_superuser:
            if user.is_active:
                login(request, user)
                return redirect('donation_list')
            else:
                messages.info(request, 'Invalid Login Details')
                return redirect('login')
        else:
            messages.info(request, 'Invalid Login Details')
            return redirect('login')
    elif request.user.is_authenticated:
        return redirect('donation_list')
    else:
        context = {
            'page_title': 'Login',
            'nbar': 'login',
        }
        return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST['UserName']
        email = request.POST['Email']
        password1 = request.POST['Password']
        password2 = request.POST['ConfirmPassword']
        if password1 == password2 and len(username) <= 150 and len(
                password1) >= 8 and password1 != username and password1 != email and not password1.isdigit() and ' ' not in username:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email)
                user.save()
                role = Role.objects.create(user_data=user)
                role.save()
                return redirect('login')
        else:
            messages.info(request, 'follow registration instructions')
            return redirect('register')
    else:
        context = {
            'page_title': 'Register',
        }
        return render(request, 'register.html', context)


def donation_list(request):
    if request.method == 'POST':
        donation_id = request.POST["donation_id"]
        review = request.POST["review"]
        Donation.objects.filter(id=donation_id).update(review_per_donation=review)
        return redirect('donation_list')
    else:
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            patient = Donation.objects.filter(patient_data=request.user)
            context = {
                'nbar': 'dashboard',
                'dbar': 'donation_list',
                'page_title': 'Donation List',
                'patient': patient
            }
            return render(request, 'donation_list.html', context)


def update_profile(request):
    if request.method == 'POST':
        username = request.POST['UserName']
        old_password = request.POST['OldPassword']
        password1 = request.POST['InputPassword1']
        password2 = request.POST['InputPassword2']
        user = authenticate(request, username=username, password=old_password)
        if user is not None:
            if user.is_active:
                if password1 == password2:
                    password = make_password(password1, hasher='default')
                    User.objects.filter(id= user.id).update(password=password)
                    return redirect('update_profile')
                else:
                    messages.info(request, 'Invalid Details')
                    return redirect('update_profile')
            else:
                messages.info(request, 'Invalid Details')
                return redirect('update_profile')
        else:
            messages.info(request, 'Invalid Details')
            return redirect('update_profile')

    else:
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            context = {
                'nbar': 'dashboard',
                'dbar': 'update_profile',
                'page_title': 'Update Profile',
            }
            return render(request, 'update_profile.html', context)


def donated_to(request):
    if not request.user.is_authenticated or request.user.userprofile.role != "Donor":
        return redirect('login')
    else:
        confirmation_id = request.GET.get('confirmation')
        print(confirmation_id)
        if confirmation_id:
            Donation.objects.filter(id=confirmation_id).update(donation_status=True)

        donor = Donation.objects.filter(donor_data=request.user)
        context = {
            'nbar': 'dashboard',
            'dbar': 'donated_to',
            'page_title': 'Donated To',
            'donor': donor
        }
        return render(request, 'donated_to.html', context)


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        logout(request)
        return redirect('login')


def searching(request):
    location = request.GET.get('location')
    blood = request.GET.get('blood')
    disease = request.GET.get('disease')

    donor_list = Donor.objects.all()

    if location:
        donor_list = donor_list.filter(location__contains=location)
    if blood:
        if blood.endswith('p'):
            blood = blood.replace('p', '+')
        elif blood.endswith('m'):
            blood = blood.replace('m', '-')
        donor_list = donor_list.filter(blood_group__contains=blood)
    if disease:
        disease = True if disease == 'True' else False
        donor_list = donor_list.filter(disease__exact=disease)

    paginated_donor_list = Paginator(donor_list, 100)
    page_num = request.GET.get('page', 1)
    try:
        page = paginated_donor_list.page(page_num)
    except EmptyPage:
        page = paginated_donor_list.page(1)

    context = {
        'nbar': 'search',
        'page_title': 'Search',
        'donor_list': page
    }
    return render(request, 'Search.html', context)


def donor_registration(request):
    if request.method == 'POST':
        phone = request.POST['phoneNumber']
        disease = request.POST['disease']
        location = request.POST['location']
        voter_card_front = request.FILES['voter_card_front']
        voter_card_back = request.FILES['voter_card_back']

        fs = FileSystemStorage()
        font_file = fs.save(voter_card_front.name, voter_card_front)

        front_uploaded_file_url = str(fs.url(font_file)).split('/')[2]
        front_uploaded_file_url = os.path.join(BASE_DIR, 'media', front_uploaded_file_url)

        voter_front_data = ocr_voter_id_front(request, front_uploaded_file_url)

        voter_id = voter_front_data['voter_id']
        first_name = voter_front_data['first_name']
        dob = voter_front_data['dob']

        os.remove(front_uploaded_file_url)

        file = fs.save(voter_card_back.name, voter_card_back)

        back_uploaded_file_url = str(fs.url(file)).split('/')[2]
        back_uploaded_file_url = os.path.join(BASE_DIR, 'media', back_uploaded_file_url)

        blood_group = ocr_voter_id_back(request, back_uploaded_file_url)

        os.remove(back_uploaded_file_url)

        print(voter_id, blood_group, first_name, dob)

        if voter_id and blood_group and first_name and dob:
            context = {
                'nbar': 'dashboard',
                'page_title': 'Donor Confirm Registration',
                'form_data': {'name': first_name, 'phone': phone, 'dob': dob, 'voter_id': voter_id,
                              'blood_group': blood_group, 'disease': disease,
                              'location': location}
            }
            return render(request, 'confirm_donor_registration.html', context)
        else:
            messages.info(request, 'upload clear picture')
            return redirect('donor_registration')
    context = {
        'nbar': 'dashboard',
        'page_title': 'Donor Registration',
    }
    if request.user.is_authenticated:
        if request.user.userprofile.role == "Donor":
            return redirect('donation_list')
        else:
            return render(request, 'donor_registration.html', context)
    else:
        return redirect('donation_list')


def ocr_voter_id_front(request, file_url):
    voter_id = ''
    first_name = ''
    dob = ''
    try:
        pytesseract.pytesseract.tesseract_cmd = os.path.join(BASE_DIR, 'Tesseract-OCR', 'tesseract.exe')
        img = cv2.imread(file_url)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        voter_data = pytesseract.image_to_string(img, lang='eng')
        print(voter_data)
    except:
        print('something error occurred')

    try:
        voter_id = voter_data.split("IDNO:")[1].split()[0]
        voter_id = voter_id.strip()
    except:
        pass

    if voter_id is None or not voter_id:
        try:
            voter_id = voter_data.split("ID NO:")[1].split()[0]
            voter_id = voter_id.strip()
        except:
            pass

    if voter_id is None or not voter_id:
        try:
            voter_id = voter_data.split("NID No")[1].split()[:3]
            voter_id = ' '.join(voter_id)
            voter_id = voter_id.strip()
        except:
            pass

    try:
        first_name = voter_data.split("Name:")[1].split()[:2]
        first_name = ' '.join(first_name)
        first_name = first_name.strip()
    except:
        pass
    if first_name is None or not first_name:
        try:
            first_name = voter_data.split("Name")[1].split()[:2]
            first_name = ' '.join(first_name)
            first_name = first_name.strip()
        except:
            pass

    try:
        dob = voter_data.split("Date of Birth:")[1].split()[:3]
        dob = ' '.join(dob)
        dob = dob.strip()
    except:
        pass
    if dob is None or not dob:
        try:
            dob = voter_data.split("Date of Birth ")[1].split()[:3]
            dob = ' '.join(dob)
            dob = dob.strip()
        except:
            pass
    return {'voter_id': voter_id, 'first_name': first_name, 'dob': dob}


def ocr_voter_id_back(request, file_url):
    blood_group = ''
    try:
        pytesseract.pytesseract.tesseract_cmd = os.path.join(BASE_DIR, 'Tesseract-OCR', 'tesseract.exe')
        img = cv2.imread(file_url)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        voter_data = pytesseract.image_to_string(img, lang='eng')
    except:
        print('something error occurred')
    try:
        blood_group = voter_data.split("Blood Group:")[1].split()[0]
    except:
        pass
    return blood_group.strip()


def confirm_donor_registration(request):
    if request.method == 'GET':
        return redirect('donor_registration')
    elif request.method == 'POST':
        phone = request.POST['phoneNumber']
        voter_id = request.POST['voterID']
        blood_group = request.POST['BloodGroup']
        disease = request.POST['disease']
        disease = False if disease == 'none' else True
        location = request.POST['location']
        first_name = request.POST['nameInput']
        dob = request.POST['dob']
        if phone is None or voter_id is None or blood_group is None or disease is None or location is None or first_name is None or dob is None:
            messages.info(request, 'some error occurred')
            return redirect('donor_registration')
        else:
            if Donor.objects.filter(voter_id=voter_id) or Donor.objects.filter(phone=phone):
                messages.info(request, 'duplicate user found')
                return redirect('donor_registration')
            else:
                User.objects.filter(username=request.user.username).update(first_name=first_name)
                donor = Donor.objects.create(donor_data=request.user, dob=dob, phone=phone, voter_id=voter_id,
                                             blood_group=blood_group,
                                             disease=disease, location=location, donor_register_date=datetime.now())
                UserProfile.objects.filter(user_data=request.user).update(role='Donor')
                donor.save()
                return redirect('donation_list')


def appointment(request):
    if request.method == 'POST' and request.user.is_authenticated:
        donor = request.POST["donorID"]
        appointment_date = request.POST['appointmentTime']
        patient = request.user.id
        if donor is patient:
            messages.info(request, "Donor can't donate thyself")
            return redirect('searching')
        else:
            donor_object = User.objects.get(id=donor)
            patient_object = User.objects.get(id=patient)
            donation = Donation.objects.create(donor_data=donor_object, patient_data=patient_object,
                                               donation_date=datetime.now(), appointment_date=appointment_date)
            donation.save()
        return redirect('donation_list')
    else:
        id = request.GET.get('id')
        if id is not None and request.user.is_authenticated:
            try:
                single_donor = Donor.objects.get(donor_data=id)
                user = User.objects.get(id=single_donor.donor_data.id)
                review_five_star = Donation.objects.filter(donor_data=user, review_per_donation__exact=5).count()
                review_four_star = Donation.objects.filter(donor_data=user, review_per_donation__exact=4).count()
                review_three_star = Donation.objects.filter(donor_data=user, review_per_donation__exact=3).count()
                review_two_star = Donation.objects.filter(donor_data=user, review_per_donation__exact=2).count()
                review_one_star = Donation.objects.filter(donor_data=user, review_per_donation__exact=1).count()
                total_review_count = review_five_star + review_four_star + review_three_star + review_two_star + review_one_star
                if total_review_count > 0:
                    avg_review = (review_five_star * 5 + review_four_star * 4 + review_three_star * 3 + review_two_star * 2 + review_one_star) / total_review_count
                else:
                    avg_review = 0

            except Donor.DoesNotExist:
                return redirect('searching')
            context = {
                'nbar': 'search',
                'page_title': 'Appointment',
                'donor': single_donor,
                'avg_review': avg_review
            }
            return render(request, 'appointment.html', context)
        else:
            return redirect('searching')


def update_phone(request):
    if request.method == "POST":
        phone = request.POST["phoneNumber"]
        if phone is not None:
            Donor.objects.filter(donor_data=request.user).update(phone=phone)
            return redirect('update_profile')
        else:
            return redirect('update_profile')
    else:
        return redirect('update_profile')