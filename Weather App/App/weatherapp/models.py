from django.db import models

class WeatherReport(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    forecast_date = models.DateTimeField()
    
