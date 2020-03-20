from django.db import models

# Create your models here.
class Customers(models.Model):
    bank_system_roles = (
        (0, 'Customer'),
        (1, 'Manager'),
        (2, 'Sales'),
        (3, 'Investment Analyst')
    
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    age = models.IntegerField()
    roles = models.IntegerField(choices=bank_system_roles, default = 0)

    def __str__(self):
        return self.first_name


class Transaction(models.Model):
    user = models.ForeignKey(Customers, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deposit_amount = models.IntegerField(null=True, blank=True)
    withdrawal_amount = models.IntegerField(null=True, blank=True)
    net_amount = models.IntegerField(default = 0,null=True, blank=True)