from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    class Meta:
        ordering = ['-id']

    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5
    name = models.CharField(max_length=50, null=False)
    slug = models.SlugField(null=False, default='', unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=False)
    rating = models.PositiveIntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value)
    discount = models.PositiveIntegerField(default=0, blank=True, null=True)
    image = models.ImageField(upload_to='media', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(null=False)
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    class Meta:
        ordering = ['-id']
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(null=False)
    body = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_appropriate = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.name

# Create your models here.


class OrderItem(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)