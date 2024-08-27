from django.db import models
from users.models import User
from django.core.validators import validate_email

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='payments')
    event = models.CharField(max_length=255)    
    deadline = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.user.username} - ${self.amount}'