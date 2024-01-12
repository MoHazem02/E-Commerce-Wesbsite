from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Category, Comment, Bid, Watchlist
from django.shortcuts import get_object_or_404


def index(request):
    return render(request, "auctions/index.html", {"Listings" : Listing.objects.all()})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid_value = request.POST["initial_bid"]
        bid = Bid(price=bid_value, bidder = None)
        bid.save()
        category_item = request.POST["category"]
        if category_item == "":
            category_item = None
        image = request.POST["image_url"]
        owner_name = request.POST["owner"]
        owner = User.objects.get(username = owner_name)
        if category_item:
            category, created = Category.objects.get_or_create(name=category_item)
            category.save()
            item = Listing(title=title, description = description, price = bid, category = category, image = image, owner = owner)
            item.save()
        else:
            item = Listing(title=title, description = description, price = bid, image = image, owner = owner)
            item.save()
        return index(request)
    else:
        return render(request, "auctions/create_listing.html")
    
def categories(request):
    category_items = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": category_items})


@login_required
def watchlist(request):
    if request.method == "POST":
        if 'Close' in request.POST:
            item_id = request.POST["listing_id"]
            item = Listing.objects.get(pk = item_id)
            item.active = False
            bid = item.price
            winner = bid.bidder
            item.buyer = winner
            item.save()
            return index(request)

        if 'place_bid' in request.POST:
            price = request.POST["User_Bid"]
            if price == "":
                return HttpResponse("Error Can't Bid with nothing")
            item_id = request.POST["listing_id"]
            item = Listing.objects.get(pk = item_id)
            if int(price) == (item.price.price):
                return HttpResponse("Error. Your bid must be higher than the current bid!")
            buyer_name = request.POST['bidder']
            buyer_object = User.objects.get(username=buyer_name)
            new_Bid = Bid(price=price, bidder=buyer_object)
            new_Bid.save()
            item.price = new_Bid
            item.save()
            return render(request, "auctions/temp_listing.html", {"item":get_object_or_404(Listing, pk = item_id), "Comments": Comment.objects.all()})
        
        elif 'add_watchlist' in request.POST:
            item_id = request.POST["listing_id"]
            item = Listing.objects.get(pk = item_id)
            
            if request.POST["add_watchlist"] == "Remove from Watchlist":
                user_watchlist = Watchlist.objects.get(watcher=request.user)
                user_watchlist.items.remove(item)
                user_watchlist.save()
                listings = user_watchlist.items.all()
                return render(request, "auctions/watchlist.html", {"items": listings})
            else:
                # Get the Watchlist object for the current user, or create a new one if it does not exist.
                watchlist, created = Watchlist.objects.get_or_create(watcher=request.user)
                watchlist.items.add(item)
                watchlist.save()
                listings = watchlist.items.all()
                return render(request, "auctions/watchlist.html", {"items": listings})

        else:
            return HttpResponse("Error Occurred!")
    else:
        user_watchlist = Watchlist.objects.get(watcher=request.user)
        watchlist_items = user_watchlist.items.all()
        return render(request, "auctions/watchlist.html", {"items": watchlist_items})


def temp_listing(request, id):
    watchlist, created = Watchlist.objects.get_or_create(watcher=request.user)
    ids = []
    for item in watchlist.items.all():
        ids.append(item.pk)
    if request.method == "POST":
        text = request.POST["User_Comment"]
        if text == "":
            pass
        else:
            user_name = request.POST["username"]
            username = User.objects.get(username = user_name)
            listing_item = Listing.objects.get(pk = id)
            comment = Comment(commentor=username, text = text, listing = listing_item)
            comment.save()
    return render(request, "auctions/temp_listing.html", {"item":get_object_or_404(Listing, pk = id), "Comments": Comment.objects.all(), "ids":ids})
        

def temp_category(request, categ):
    category = Category.objects.get(name=categ)
    items = Listing.objects.filter(category=category)
    return render(request, "auctions/index.html", {"Listings" : items, "CATEGORY":categ})

