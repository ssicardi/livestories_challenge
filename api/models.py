from django.db import models
from django.db.models import Count

# Create your models here.
class Events(models.Model):
	event_type = models.CharField(max_length=250)
	date = models.DateTimeField('date')

	def getHour(self):
		return self.date.strftime('%H')