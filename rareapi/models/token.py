from django.db import models

class Token(models.Model):
  user = models.OneToOneField("RareUser", on_delete=models.CASCADE)
  created = models.CharField(max_length=50)