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
        # print(ratings)
        # ratings = {}
        # five,four,three,two,one=0,0,0,0,0
        # rev = Reviews.objects.filter(product=self.id)
        # for i in rev:
        #     if i.rating==5:
        #         five+=1
        #     elif i.rating==4:
        #         four+=1
        #     elif i.rating==3:
        #         three+=1
        #     elif i.rating==2:
        #         two+=1
        #     elif i.rating==1:
        #         one+=1

        # ratings.update({5:five})
        # ratings.update({4:four})
        # ratings.update({3:three})
        # ratings.update({2:two})
        # ratings.update({1:one})

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
    date = models.DateField(auto_now_add=True)
    options = (
        ('in-cart','in-cart'),
        ('order-placed', 'order-placed'),
        ('removed', 'removed')
    )
    status = models.CharField(max_length=100, choices=options, default='in-cart')