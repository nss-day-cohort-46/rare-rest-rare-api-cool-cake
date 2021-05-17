"""Tag Model"""
from django.db import Models


class Tag(models.Model):
	"""Tag Model"""
	label = models.CharField(max_length=50)

