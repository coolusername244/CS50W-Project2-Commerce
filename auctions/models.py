from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def category_check(value):
    # 14 = Please Select
    if value == 14:
        raise ValidationError(
            _('Please select a category'),
            params={'value': value},
        )

def condition_check(value):
    # 1 = Please Select
    if value == 1:
        raise ValidationError(
            _('Please select a condition'),
            params={'value': value},
        )

class User(AbstractUser):
    pass


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
    
    def get_friendly_name(self):
        return self.friendly_name


class Condition(models.Model):
    name = models.CharField(max_length=254, null=False)
    friendly_name = models.CharField(max_length=254, null=False)

    def __str__(self):
        return f"{self.name}"
    
    def get_friendly_name(self):
        return self.friendly_name


class Listing(models.Model):
    is_active = models.BooleanField(default=True, null=False)
    title = models.CharField(max_length=254)
    subtitle = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, validators=[MinValueValidator(1)])
    current_price = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    category = models.ForeignKey("Category", null=True, on_delete=models.SET_NULL, validators=[category_check])
    condition = models.ForeignKey("Condition", null=True, on_delete=models.SET_NULL, validators=[condition_check])
    image_url = models.URLField()
    created = models.DateTimeField(default=timezone.now, editable=False)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self):
        return f"ID: {self.id} - Item: {self.title} - Seller: {self.user}"


class Comment(models.Model):
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Listing - {self.listing}. Date - {self.date}"


class Wishlist(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user} - {self.listing}"


class Bid(models.Model):
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    bid = models.DecimalField(decimal_places=2, max_digits=20)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Listing - {self.listing}. Bid - {self.bid}"