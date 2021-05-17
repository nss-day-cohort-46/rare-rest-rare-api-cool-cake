from rest_framework.viewsets import ViewSet
from rareapi.models import RareUser, Comment

class Comment(ViewSet):
    def create(self, request):
        author = RareUser.objects.get(user = request.auth.user)

        comment = Comment()
        comment.content = request.data["content"]
        comment.created_on = request.data["createdOn"]
        comment.author = author
        