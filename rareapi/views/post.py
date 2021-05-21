"""View module for handling requests about games"""
from rareapi.models.category import Category
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from datetime import date, datetime
from rareapi.models import (Post, RareUser, PostReaction,
                            Reaction, Comment, PostTag,
                            Tag)


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
        user = request.auth.user
        if user.is_staff is True:
            post = Post.objects.all().order_by("-publication_date")

        elif user.is_staff is False:
            date_thresh = datetime.now()
            post = Post.objects.all().order_by("-publication_date").filter(approved=True).filter(
                publication_date__lt=date_thresh)

        user_id = request.query_params.get('user_id', None)
        if user_id is not None and user_id == str(user.id):
            post = Post.objects.all()
            post = post.filter(user__id=user_id)
        if user_id is not None and user_id != str(user.id):
            return Response({}, status=status.HTTP_403_FORBIDDEN)
        # # Note the additional `many=True` argument to the
        # # serializer. It's needed when you are serializing
        # # a list of objects instead of a single object.

        serializer = PostSerializer(
            post, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def react(self, request, pk=None):
        if request.method == "POST":
            post = Post.objects.get(pk=pk)
            user = RareUser.objects.get(user=request.auth.user)
            reaction = Reaction.objects.get(pk=request.data['reactionId'])

            try:
                reacting = PostReaction.objects.get(
                    user=user, post=post, reaction=reaction
                )
                return Response(
                    {'message': 'User already used this reaction.'},
                    status=status.HTTP_204_NO_CONTENT
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
            reaction = Reaction.objects.get(pk=request.data['reactionId'])

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

    @action(methods=['get'], detail=True)
    def comments(self, request, pk=None):
        try:
            comments = Comment.objects.all()
            post = Post.objects.get(pk=pk)
            comments = comments.filter(post=post)
            serializer = CommentSerializer(
                comments, many=True, context={'request': request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized game instance
        """
        # Uses the token passed in the `Authorization` header
        user = request.auth.user
        category = Category.objects.get(pk=request.data["categoryId"])
        # tags = PostTag.objects.get(pk=request.data["tagId"])
        # reactions = PostReaction.objects.get(pk=request.data["reactionId"])

        post = Post()
        post.user = user
        post.category = category
        post.title = request.data["title"]
        post.publication_date = datetime.now()
        post.image_url = request.data["imageUrl"]
        post.content = request.data["content"]
        post.approved = False
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
        # category = Category.objects.get(pk = request.data["categoryId"])
        post = Post.objects.get(pk=pk)

        if user != post.user:
            return Response({}, status=status.HTTP_403_FORBIDDEN)

        post.user = user
        post.category = Category.objects.get(pk=request.data["categoryId"])
        post.title = request.data["title"]

        post.image_url = request.data["imageUrl"]
        post.content = request.data["content"]

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

    @action(methods=["put"], detail=True)
    def approve(self, request, pk=None):
        """Managing admin approving post"""

        user = request.auth.user
        if not user.is_staff:
            return Response({}, status=status.HTTP_403_FORBIDDEN)

        if request.method == "PUT":
            post = Post.objects.get(pk=pk)

            if post.approved:
                return Response({}, status=status.HTTP_304_NOT_MODIFIED)

            try:
                post.approved = True
                post.save()
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            except:
                return Response(
                    {'message': 'Post does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_on')


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts

    Arguments:
        serializer type
    """
    user = UserSerializer(many=False)

    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date',
                  'image_url', 'content', 'approved', 'tags', 'reactions')
        depth = 1
