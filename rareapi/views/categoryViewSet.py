"""Category ViewSet"""
from django.http import HttpResponseServerError
from django.db.models.functions import Lower

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status

from .categorySerializer import CategorySerializer
from rareapi.models import Category

from rareapi.models import RareUser


class CategoryViewSet(ViewSet):
    """
        View module for handling requests about categories.
        ViewSet handles GET, POST, PUT, DELETE requests sent from client
        over HTTP protocol.

        Category ViewSet
    """

    def create(self, request):
        """
            Handle POST requests for categories.
            Returns:
                Response -- JSON serialized even instance.
        """

        category = Category()
        category.label = request.data['label']

        try:
            category.save()
            serialized_category = CategorySerializer(
                category, context={'request': request})
            return Response(serialized_category.data)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_404_NOT_FOUND)

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

    def destroy(self, request, pk=None):
        """
            Handle DELETE request for a single category.
            Returns:
                Response - 200, 204, 500 status code.
        """

        try:
            category = Category.objects.get(pk=pk)
            user = request.auth.user
            if user.is_staff:
                category.delete()

                return Response({}, status=status.HTTP_204_NO_CONTENT)

            else:
                return Response({'message': "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """
            Handle PUT request for a category.
            Returns:
                Response -- Empty body with 204 status code.
        """


        try:
            category = Category.objects.get(pk=pk)
            user = request.auth.user

            if user.is_staff:
                category.label = request.data["label"]
                category.save()

                # 204 - everything worked but server has nothing to send back
                # in response
                return Response({}, status=status.HTTP_204_NO_CONTENT)

            else:
                return Response({'message': "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)