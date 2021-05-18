"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Post
from django.contrib.auth.models import User



class PostView(ViewSet):
    """Rare posts"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        post = Post.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = PostSerializer(
            post, many=True, context={'request': request})
        return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts

    Arguments:
        serializer type
    """
    user = UserSerializer(many=False)

    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved', 'tags', 'reactions' )
        depth = 1
        