"""Category ViewSet"""
from django.http import HttpResponseServerError
from django.db.models.functions import Lower

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status

from .categorySerializer import CategorySerializer
from rareapi.models import Category


class CategoryViewSet(ViewSet):
    """
        View module for handling requests about categories.
        ViewSet handles GET, POST, PUT, DELETE requests sent from client
        over HTTP protocol.

        Category ViewSet
    """

    def retrieve(self, request, pk=None):
        """
            Handle GET requests for single category.
            Returns:
                Response : JSON serialized category.
        """
        try:
            category = Category.objects.get(pk=pk)
            serialized_category = CategorySerializer(category,
                                                     context={'request': request})
            return Response(serialized_category.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
            Handle GET requests to get all categories resources.
            Returns:
                Response : JSON serialized list of category types.
        """

        try:
            categories = Category.objects.all().order_by(Lower('label'))
            serialzied_categories = CategorySerializer(
                categories,
                many=True,
                context=({'request': request})
            )
            return Response(serialzied_categories.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
