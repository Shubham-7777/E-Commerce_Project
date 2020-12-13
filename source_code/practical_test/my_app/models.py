from django.db import models
from django.conf import settings
from django.shortcuts import reverse


# Create your models here.

User = settings.AUTH_USER_MODEL

CATEGORY_CHOICES = (
    ('S', 'Shoes'),
    ('FV', 'Fruits and Vegetables'),
    ('MV', 'Meat and Fish'),
    ('C', 'Cooking'),
    ('B', 'Beverages'),
    ('HC', 'Home and Cleaning'),
    ('PC', 'Pest Control'),
    ('OP', 'Office Products'),
    ('BP', 'Beauty Products'),
    ('HP', 'Health Products'),
    ('PC', 'Pet Care'),
    ('HA', 'Home Appliances'),
    ('BC', 'Baby Care')
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    alternate_mobile_no = models.DecimalField(max_digits=10, decimal_places=10, null=True, blank=True)


class Item(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("my_app:detail_page_url_name", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("my_app:add_to_cart_url_name", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("my_app:remove_from_cart_url_name", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField()
    payment = models.FloatField(default=1000)
    delivered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('my_app.ShippingAddress', on_delete=models.CASCADE, blank=True, null=True)

    def get_total(self):
        total = 0
        for obj in self.items.all():
            total += obj.get_final_price()
        return total


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    e_mail = models.CharField(max_length=50)
    phone_number = models.DecimalField(max_digits=10, decimal_places=10)
    country = models.CharField(max_length=15)
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=15)
    address_line1 = models.CharField(max_length=250)
    address_line2 = models.CharField(max_length=250, default="No address")
    postal_code = models.DecimalField(max_digits=5, decimal_places=5)
