from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):

    category_choice = [
        ('Внедорожник', 'Внедорожник'),
        ('Седан', 'Седан'),
        ('Купе', 'Купе'),
        ('Хэтчбек', 'Хэтчбек')
    ]

    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    category = models.CharField(max_length=100, choices=category_choice, default='SEDAN')
    image = models.ImageField(upload_to='cars/images/', null=True, blank=True)

    def __str__(self):
        return f"{self.make} {self.model}"



class Comment(models.Model):
    content = models.TextField
    created_at = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(Car, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
