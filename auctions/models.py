from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
    

class Bid(models.Model):
    price = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="Bids_Made")

    def __str__(self) -> str:
        return str(self.price)


class Listing(models.Model):
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=300)
    price = models.ForeignKey(Bid, on_delete=models.PROTECT, null=True)    
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True,  related_name="category_items")
    image = models.CharField(max_length=250, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="items_listed_by_user")
    active = models.BooleanField(default=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="items_won")
    

    def __hash__(self):
        return hash(self.pk)

    def __str__(self) -> str:
        return self.title
    

class Watchlist(models.Model):
    watcher = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="watchlist")
    items = models.ManyToManyField(Listing, blank=True, null=True)

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, related_name="listing_comments")
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=300, default="Empty")

    def __str__(self) -> str:
        return f"{self.commentor}: {self.text}"
        

