from django.db import models
import datetime

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.first_name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items = models.TextField(null=True)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField(auto_now=True)

    def __str__(self) -> str:
        return self.items

