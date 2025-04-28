from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets



class User(AbstractUser):
    is_active = models.BooleanField(default=False)

class UserConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, default=secrets.token_hex(3).upper())
    created_at = models.DateTimeField(auto_now_add=True)


class category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

STARS = [
    (i, '⭐' * i) for i in range(1, 6)  # Пример с эмодзи
]

class review(models.Model):
    text = models.CharField(max_length=255)
    product = models.ForeignKey(product, on_delete=models.CASCADE,
                                related_name='reviews')
    stars = models.IntegerField(choices=STARS, default=5)

    def __str__(self):
        return self.text