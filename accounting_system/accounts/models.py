"""
    Module name :- models
    Classes :- TransactionModel
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TransactionModel(models.Model):
    """
        Data model for transaction.
    """
    CATEGORY = [
        ('food', 'Food'),
        ('rent', 'Rent'),
        ('picnic', 'Picnic'),
        ('credit', 'Credit'),
        ('debit', 'Debit')
    ]
    PAYMENT_MODE = [
        ('upi','UPI'),
        ('cash','Cash'),
        ('net banking','Net Banking'),
        ('credit card','Credit Card'),
        ('debit card','Debit Card')
    ]

    username = models.OneToOneField(User, on_delete = models.CASCADE)
    date = models.DateField(auto_now=True)
    category = models.CharField(max_length=100, choices=CATEGORY)
    description = models.TextField(blank=True)
    amount = models.FloatField()
    mode_of_payment = models.CharField(max_length=15, choices=PAYMENT_MODE)
