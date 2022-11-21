from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    Brand = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images', null=True)
    category = models.CharField(max_length=100)

    @property
    def avg_rating(self):
        ratings = self.reviews_set.all().values_list("rating", flat=True)
        if ratings:
            return(sum(ratings)/len(ratings))
        return 0
    
    @property
    def review(self):
        return self.reviews_set.all()


    @property
    def rating_count(self):
        ratings=self.reviews_set.all().values_list('rating').annotate(bit=Count('rating'))
        return ratings

    def __str__(self):
        return self.name

class Reviews(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    

    def __str__(self):
        return self.comment

class Carts(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    options = (
        ('in-cart','in-cart'),
        ('order-placed', 'order-placed'),
        ('removed', 'removed')
    )
    status = models.CharField(max_length=100, choices=options, default='in-cart')