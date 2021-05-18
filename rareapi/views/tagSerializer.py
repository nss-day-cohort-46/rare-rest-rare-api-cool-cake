from rest_framework import serializers

from rareapi.models import Tag

class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for Tags"""

    class Meta:
        model = Tag
        fields = ('id', 'label')
