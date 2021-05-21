from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.core.exceptions import ValidationError
from rareapi.models import Reaction
import json

class Reactions(ViewSet):
    def create(self, request):
        user = request.auth.user
        if not user.is_staff:
            data = json.dumps({"admin": False})
            return Response(data, content_type='application/json', status=status.HTTP_403_FORBIDDEN)

        reaction = Reaction()
        reaction.label = request.data["label"]
        reaction.image_url = request.data["imageUrl"]

        try:
            reaction.save()
            serializer = ReactionSerializer(reaction, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_404_BAD_REQUEST)

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')