from django.db import models
from django.utils.timezone import now

class ClientRecord(models.Model):

	clientID = models.CharField(max_length=10, blank=False)
	calloutDate = models.DateField(default=now, editable=True)
	## Need to be in special form. For example: Interested in A, B, C;Not Interested in X, X, X
	Uniformfield = models.TextField(default="")
	## No special rules, can be some chat or conversation
	Nonuniformfield = models.TextField(default="")

	def __str__(self):
		return self.Uniformfield
