from django.shortcuts import render, redirect
from blog.models import Post  
from django.contrib import messages
from .models import ContactMessage


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def leadership(request):
    return render(request, 'leadership.html')

def achievements(request):
    return render(request, 'achievements.html')

def contact(request):
    return render(request, 'contact.html')

def history(request):
    return render(request, 'history.html')

def manifesto(request):
    return render(request, 'manifesto.html')

def constituencies(request):
    return render(request, 'constituencies.html')


def home(request):
    latest_news = Post.objects.filter(is_published=True).order_by('-created_at')[:3]
    return render(request, 'home.html', {'latest_news': latest_news})


def contact(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get("name", "").strip(),
            email=request.POST.get("email", "").strip(),
            phone=request.POST.get("phone", "").strip(),
            subject=request.POST.get("subject", "").strip(),
            message=request.POST.get("message", "").strip(),
        )
        messages.success(
            request,
            "Your message has been sent successfully. We will get back to you soon.",
        )
        return redirect("contact")

    return render(request, "contact.html")

def privacy(request):
    return render(request, "privacy.html")


def terms(request):
    return render(request, "terms.html")