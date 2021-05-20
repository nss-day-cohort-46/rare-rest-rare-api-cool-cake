import json
from django.contrib.auth.models import User
from django.db.models.functions import Lower
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
            data = json.dumps({"admin":False})
            return Response(data, content_type='application/json', status=status.HTTP_403_FORBIDDEN)

        users = User.objects.all().order_by(Lower('first_name'))
        
        serializer = UserSerializer(
            users, many=True, context={'request': request}
        )

        return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for django user model"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'is_staff')

# class RareUserSerializer(serializers.ModelSerializer):
#     """JSON serializer for for rareUser model"""
#     user =UserSerializer(many=False)

#     class Meta:
#         model = RareUser
#         fields()