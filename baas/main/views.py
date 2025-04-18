from django.shortcuts import render

def landingpage(request):
    return render(request, "main\landingpage.html")

def about(request):
    return render(request, "main/about.html")

def shop(request):
    return render(request, "main/shop.html")

def contact(request):
    return render(request, "main/contact.html")