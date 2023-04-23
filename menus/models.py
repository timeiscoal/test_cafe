from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class MenuSize(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class Menu(models.Model):
    categories = models.ForeignKey(Category, on_delete=models.SET_DEFAULT , default="1")
    price = models.PositiveIntegerField(default=0)
    cost = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    barcode = models.TextField()
    expiration_date = models.DateTimeField()
    size = models.ForeignKey(MenuSize, on_delete=models.SET_DEFAULT, default="1")

    def __str__(self) -> str:
        return self.name