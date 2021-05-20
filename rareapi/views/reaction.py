from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.core.exceptions import ValidationError
from rareapi.models import Reaction

class Reactions(ViewSet):
    def create(self, request):
        reaction = Reaction()
        reaction.label = request.data["label"]
        reaction.image_url = request.data["imageUrl"]

        try:
            reaction.save()
            serializer = ReactionSerializer(reaction, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_404_BAD_REQUEST)

    def list(self, request):
        reactions = Reaction.objects.all()
        serializer = ReactionSerializer(
            reactions, many=True, context={'request': request}
        )
        return Response(serializer.data)

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')