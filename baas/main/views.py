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

def cart(request):
    return render(request, "main/cart.html")

def charging_hub(request):
    embed_url = None
    place = None
    if request.method == "POST":
        place = request.POST.get("search")
        if place:
            search_query = f"{place} EV charging stations"
            embed_url = f"https://maps.google.com/maps?q={search_query.replace(' ', '+')}&output=embed"
    
    return render(request, "main/charging_hub.html", {"embed_url": embed_url, "place" : place})
