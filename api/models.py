from django.db import models

# Create your models here.
class Events(models.Model):
	event_type = models.CharField(max_length=250)
	date = models.DateTimeField('date')