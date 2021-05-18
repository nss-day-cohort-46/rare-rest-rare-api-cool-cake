"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Post, RareUser, PostReaction, Reaction



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
    
    @action(methods=['post', 'delete'], detail=True)
    def react(self, request, pk=None):
        if request.method == "POST":
            post = Post.objects.get(pk=pk)
            user = RareUser.objects.get(user=request.auth.user)
            reaction = Reaction.objects.get(pk = request.data['reactionId']) 

            try:
                reacting = PostReaction.objects.get(
                    user=user, post=post, reaction=reaction
                )
                return Response(
                    {'message': 'User already used this reaction.'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except PostReaction.DoesNotExist:
                reacting = PostReaction()
                reacting.post = post
                reacting.user = user
                reacting.reaction = reaction
                reacting.save()

                return Response({}, status=status.HTTP_201_CREATED)
        
        elif request.method == "DELETE":
            try:
                post = Post.objects.get(pk=pk)
            except Post.DoesNotExist:
                return Response(
                    {'message': 'Post does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = RareUser.objects.get(user=request.auth.user)
            reaction = Reaction.objects.get(pk = request.data['reactionId'])

            try:
                reacting = PostReaction.objects.get(
                    user=user, post=post, reaction=reaction
                )
                reacting.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)

            except PostReaction.DoesNotExist:
                return Response(
                    {'message': 'User has not used this reaction.'},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts

    Arguments:
        serializer type
    """
    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved', 'tags', 'reactions' )
        
  