from django.shortcuts import render


# Create your views here.
def home(request):
    context = {
        'nbar': 'index',
        'donor_list': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    return render(request, 'index.html', context)
