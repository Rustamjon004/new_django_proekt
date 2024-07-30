from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    class RatingChoices(models.IntegerChoices):
        ZERO = 0
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image=models.ImageField(upload_to='products',null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField(default=0)
    rating = models.PositiveSmallIntegerField(choices=RatingChoices.choices, default=RatingChoices.ZERO.value,null=True,blank=True)
    discount = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

    def __str__(self):
        return self.name



class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.username


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Order(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('sending', 'sending'),
        (' fast delivered', ' fast delivered'),
        ('be canceled', ' BE canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status

    from django.contrib.auth.models import AbstractUser



    def check_for_profanity(self):

        profane_words = ["haqoratli_soz1", "haqoratli_soz2", "haqoratli_soz3"]
        content_lower = self.content.lower()

        for word in profane_words:
            if word in content_lower:
                self.warn_user()
                self.block_user()
                return True

        return False

    def warn_user(self):
        print(f"Ogohlantirish: Foydalanuvchi {self.user} haqoratli so'zlar ishlatgan.")

    def block_user(self):
        self.is_blocked = True
        self.save()
        print(f"Foydalanuvchi {self.user} bloklandi.")

