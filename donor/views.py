import os
from pathlib import Path
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from donor.models import UserProfile as Role
import cv2
import pytesseract

# Create your views here.
from greenlife import settings

BASE_DIR = Path(__file__).resolve().parent.parent


def home(request):
    context = {
        'page_title': 'Home',
        'nbar': 'index',
        'donor_list': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    return render(request, 'index.html', context)


def view_login(request):
    if request.method == 'POST':
        username = request.POST['User']
        password = request.POST['Password']
        print(username, password)
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
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        context = {
            'nbar': 'dashboard',
            'dbar': 'donation_list',
            'page_title': 'Donation List',
        }
        return render(request, 'donation_list.html', context)


def update_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        context = {
            'nbar': 'dashboard',
            'dbar': 'update_profile',
            'page_title': 'Update Profile',
        }
        return render(request, 'update_profile.html', context)


def review(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        context = {
            'nbar': 'dashboard',
            'dbar': 'review',
            'page_title': 'Review',
        }
        return render(request, 'review.html', context)


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        logout(request)
        return redirect('login')


def searching(request):
    donor_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
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
        voter_card = request.FILES['voter_card']
        fs = FileSystemStorage()
        file = fs.save(voter_card.name, voter_card)
        uploaded_file_url = str(fs.url(file)).split('/')[2]
        uploaded_file_url = os.path.join(BASE_DIR, 'media', uploaded_file_url)
        temp_data = ocr_voter_id(request,uploaded_file_url)
        os.remove(uploaded_file_url)
        voter_id = temp_data['voter_id']
        blood_group = temp_data['blood_group']
        print(voter_id, blood_group)
        if voter_id and blood_group:
             pass
        else:
            messages.info(request,'upload clear picture')
            return redirect('donor_registration')
    context = {
        'nbar': 'dashboard',
        'page_title': 'Donor Registration',
    }
    return render(request, 'donor_registration.html', context)


def ocr_voter_id(request, file_url):
    pytesseract.pytesseract.tesseract_cmd = os.path.join(BASE_DIR, 'Tesseract-OCR', 'tesseract.exe')
    img = cv2.imread(file_url)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    voter_data = pytesseract.image_to_string(img, lang='eng')
    voter_id = ''
    blood_group = ''

    try:
        voter_id = voter_data.split("IDNO:")[1].split()[0]
    except:
        print('something error occurred')
    try:
        blood_group = voter_data.split("Blood Group:")[1].split()[0]
    except:
        print('something error occurred')
    try:
        voter_id = voter_data.split("NID No")[1].split()[:3]
        voter_id = ' '.join(voter_id)
    except:
        print('something error occurred')
    return {'voter_id': voter_id.strip(), 'blood_group': blood_group.strip()}
