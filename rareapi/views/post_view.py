"""View module for handling requests about posts"""
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
from rest_framework.decorators import action
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

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = PostSerializer(
            post, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized game instance
        """
        # Uses the token passed in the `Authorization` header
        user = RareUser.objects.get(user=request.auth.user)
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
        user = RareUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk = request.data["categoryId"])

        post = Post.objects.get(pk=pk)
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
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=["put"], detail=True)
    def approve(self, request, pk=None):
        """Managing admin approving post"""

        user = request.auth.user
        if not user.is_staff:
            return Response({}, status=status.HTTP_403_FORBIDDEN) 
        
        if request.method == "PUT":
            post = Post.objects.get(pk=pk)
            try:    
                post.approved = True
                post.save()
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            except:
                return Response(
                    {'message': 'Post does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    Arguments:
        serializer type
    """
    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved', 'tags', 'reactions' )
        
  
