from django.shortcuts import render

def signin(request):
    return render(request, "main/signin.html")

def landingpage(request):
    return render(request, "main/landingpage.html")

def about(request):
    return render(request, "main/about.html")

def shop(request):
    return render(request, "main/shop.html")

def contact(request):
    return render(request, "main/contact.html")

def product(request, id):
    return render(request, "main/product.html", context={"product_id" : id})