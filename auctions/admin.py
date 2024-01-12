from django.contrib import admin
from .models import Listing, Category, User, Comment, Bid, Watchlist

# Register your models here.
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(User) #remove if not important
admin.site.register(Watchlist)

