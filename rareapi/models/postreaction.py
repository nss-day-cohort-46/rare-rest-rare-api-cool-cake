from django.db import models


class PostReaction(models.Model):
    user = models.OneToOneField("RareUser", on_delete=models.CASCADE)
    post = models.OneToOneField("Post", on_delete=models.CASCADE)
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE)
