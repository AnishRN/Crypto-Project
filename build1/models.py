from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profit_cap = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    loss_cap = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
