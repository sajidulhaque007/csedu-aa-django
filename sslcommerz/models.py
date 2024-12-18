from django.db import models

class SSLPayment(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    user_id = models.CharField(max_length=100,null=True)
    membershipId = models.CharField(max_length=100, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='BDT')
    cus_name = models.CharField(max_length=100)
    cus_email = models.EmailField(max_length=100)
    cus_phone = models.CharField(max_length=20)
    reference = models.CharField(max_length=20, null=True, blank=True)
    cus_address = models.CharField(max_length=255, null=True, blank=True)
    cus_city = models.CharField(max_length=255, null=True, blank=True)
    cus_country = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.transaction_id
