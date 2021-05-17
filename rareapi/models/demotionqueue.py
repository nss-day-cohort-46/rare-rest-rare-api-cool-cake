from django.db import models

class DemotionQueue(models.Model):
  action = models.CharField()
  admin = models.ForeignKey("RareUser", on_delete=models.CASCADE)
  approver_one = models.ForeignKey("RareUser", on_delete=models.CASCADE)