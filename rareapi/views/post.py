"""View module for handling requests about games"""
from rareapi.models.postreaction import PostReaction
from rareapi.models.posttag import PostTag
from rareapi.models.reaction import Reaction
from rareapi.models.tag import Tag
from rareapi.models.category import Category
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Post, RareUser
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
        user = request.query_params.get('user_id', None)
        if user is not None:
            post = post.filter(user__id=user)
        
        # # Note the additional `many=True` argument to the
        # # serializer. It's needed when you are serializing
        # # a list of objects instead of a single object.
        
        serializer = PostSerializer(
            post, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized game instance
        """
        # Uses the token passed in the `Authorization` header
        user = request.auth.user
        category = Category.objects.get(pk = request.data["categoryId"])
        # tags = PostTag.objects.get(pk=request.data["tagId"])
        # reactions = PostReaction.objects.get(pk=request.data["reactionId"])

        post = Post()
        post.user = user
        post.category = category
        post.title = request.data["title"]
        post.publication_date = request.data["publishedOn"]
        post.image_url = request.data["imageUrl"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]
        # post.tags = tags
        # post.reactions = reactions

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_404_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for a game
        Returns:
            Response -- Empty body with 204 status code
        """
        user = request.auth.user
        category = Category.objects.get(pk = request.data["categoryId"])
        post = Post.objects.get(pk=pk)


        if user != post.user:
            return Response({}, status=status.HTTP_403_FORBIDDEN)

        post.user = user
        post.category = category
        post.title = request.data["title"]
        post.publication_date = request.data["publishedOn"]
        post.image_url = request.data["imageUrl"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]

        post.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):


        try:
            post = Post.objects.get(pk=pk)
            user = RareUser.objects.get(user=request.auth.user)
            if user.user_id != post.user.id:
                return Response({}, status=status.HTTP_403_FORBIDDEN)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        