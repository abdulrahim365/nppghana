from django.shortcuts import render

# Create your views here.

def achievements_home(request):
    return render(request, 'achievements/achievements_home.html')
