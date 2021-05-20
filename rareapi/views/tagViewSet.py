"""Tag ViewSet"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from django.db.models.functions import Lower

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status

from .tagSerializer import TagSerializer
from rareapi.models import Tag

from rareapi.models import RareUser


class TagViewSet(ViewSet):
    """
        View module for handling requests about tags.
        ViewSet handles GET, POST, PUT, DELETE requests sent from client
        over HTTP protocol.

        Tag ViewSet
    """

    def create(self, request):
        """
            Handle POST requests for tags.
            Returns:
                Response -- JSON serialized even instance.
        """

        user = RareUser.objects.get(user=request.auth.user)

        tag = Tag()
        tag.label = request.data['label']

        try:
            tag.save()
            serialized_tag = TagSerializer(tag, context={'request': request})
            return Response(serialized_tag.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        """
            Handle GET requests for single tag.
            Returns:
                Response : JSON serialized tag.
        """
        try:
            # 'pk' - parameter to function
            # Django parses it from the URL
            # http://localhost:8000/tags/2
            # '2' - becomes pk
            tag = Tag.objects.get(pk=pk)
            print("pk is ", pk)
            print("tag is")
            print(tag)
            serialized_tag = TagSerializer(tag, context={'request': request})
            return Response(serialized_tag.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
            Handle GET requests to get all tag resources.
            Returns:
                Response : JSON serialized list of tag types.
        """

        tags = Tag.objects.all().order_by(Lower('label'))
        user = request.auth.user

        # filter tags by type
        # http://localhost:8000/tags?type=1
        # 1 - tabletop tags
        # tag_type = self.request.query_params.get('type', None)
        # if tag_type is not None:
        #     # Note: there are two  underscores between tagtype and
        #     # id. They denote a query join.
        #     tags = tags.fiter(tagtype__id=tag_type)

        # Note additonal 'many=True'
        # It's for serializing a list of objects instead of one.
        serialized_tags = TagSerializer(
            tags,
            many=True,
            context={'request': request}
        )

        return Response(serialized_tags.data)

    def destroy(self, request, pk=None):
        """
            Handle DELETE request for a single tag.
            Returns:
                Response - 200, 204, 500 status code.
        """

        try:
            tag = Tag.objects.get(pk=pk)
            user = request.auth.user
            if user.is_staff:
                tag.delete()

                return Response({}, status=status.HTTP_204_NO_CONTENT)

            else:
                return Response({'message': "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """
            Handle PUT request for a tag.
            Returns:
                Response -- Empty body with 204 status code.
        """


        # Simlar to POST.
        # Instead of creating new instance, update exisiting record.
        try:
            tag = Tag.objects.get(pk=pk)
            user = request.auth.user

            print("user is ")
            if user.is_staff:
                print(" satff")
                tag.label = request.data["label"]
                tag.save()

                # 204 - everything worked but server has nothing to send back
                # in response
                return Response({}, status=status.HTTP_204_NO_CONTENT)

            else:
                print(" not staff ")
                return Response({'message': "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)