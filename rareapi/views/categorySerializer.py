from rest_framework import serializers

from rareapi.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for Categories"""

    class Meta:
        model = Category
        fields = ('id', 'label')
