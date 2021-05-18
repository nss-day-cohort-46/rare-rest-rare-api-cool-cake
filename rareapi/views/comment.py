from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.core.exceptions import ValidationError
from rareapi.models import RareUser, Comment, Post

class Comments(ViewSet):
    def create(self, request):
        author = RareUser.objects.get(user = request.auth.user)
        post = Post.objects.get(pk = request.data["postId"])

        comment = Comment()
        comment.content = request.data["content"]
        comment.created_on = request.data["createdOn"]
        comment.author = author
        comment.post = post

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_404_BAD_REQUEST)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_on')