"""Tag ViewSet"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status

from .tagSerializer import TagSerializer
from rareapi.models import Tag


class TagViewSet(ViewSet):
    """
        View module for handling requests about tags.
        ViewSet handles GET, POST, PUT, DELETE requests sent from client
        over HTTP protocol.

        Tag ViewSet
    """

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

        tags = Tag.objects.all().order_by('label')

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