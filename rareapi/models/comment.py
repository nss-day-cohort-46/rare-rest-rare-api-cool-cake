from django.db import models

class Comment(models.Model):
  post = models.ForeignKey("Post", on_delete=models.CASCADE)
  author = models.ForeignKey("RareUser", on_delete=models.CASCADE)
  content = models.TextField(max_length=500)
  created_on = models.DateTimeField()