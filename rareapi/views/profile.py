import json
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.http.response import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import RareUser


class ProfileView(ViewSet):
    """Admin can see all profiles"""

    def list(self, request):
        """Handle GET request to profiles"""

        user = request.auth.user
        if not user.is_staff:
            data = json.dumps({"admin": False})
            return Response(data, content_type='application/json', status=status.HTTP_403_FORBIDDEN)

        users = User.objects.all().order_by(Lower('first_name'))

        serializer = UserSerializer(
            users, many=True, context={'request': request}
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single profile

        Returns:
            Response -- JSON serialized profile
        """
        try:
            user = User.objects.get(pk=pk)
            profile = RareUser.objects.get(pk=pk)
            profile.user = user

            if profile.profile_image_url == "['profileImageUrl']":
                profile.profile_image_url = "https://thesciencedog.files.wordpress.com/2013/09/golden-retriever-and-science1.jpg"
            serializer = RareUserSerializer(profile, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(methods=['put'], detail=True)
    def deactivate(self, request, pk=None):
        """Managing admin approving post"""

        user = request.auth.user
        if user.is_staff:
            try:
                rareuser = User.objects.get(pk=pk)

                if rareuser.is_staff:
                    return Response({}, status=status.HTTP_403_FORBIDDEN) 
            
                rareuser.is_active = False
                rareuser.save()
                return Response({}, status=status.HTTP_204_NO_CONTENT)

            except User.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({}, status=status.HTTP_403_FORBIDDEN)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for django user model"""

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'is_staff')


class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for for rareUser model"""
    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ('user', 'profile_image_url', 'created_on')
