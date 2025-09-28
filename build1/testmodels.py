from django.db import models

class Cryptocurrency(models.Model):
    ticker = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()
    timeframe = models.IntegerField()
