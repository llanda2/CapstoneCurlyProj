from django.shortcuts import render


# A simple home view for the root URL
def home(request):
    return render(request, 'home.html')
