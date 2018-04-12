from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, SnippetModelSerializer,\
SnippetDetailSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from snippets.filters import SnippetBackendFilter
from snippets.core import CustomPaginator
from rest_framework.generics import ListAPIView
from django.db import IntegrityError, transaction


class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SnippetViewSet(ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer
    filter_backends = (SnippetBackendFilter, SearchFilter, OrderingFilter)
    search_fields = ('title', 'language')
    ordering_fields = ('title', 'language')
    # pagination_class = CustomPaginator

    # @transaction.atomic
    # def create(self, request):
    #     print('> create')
    #
    #     serializer = SnippetModelSerializer(data=request.data)
    #
    #     details = request.data.get('details')
    #     print(details)
    #
    #     if serializer.is_valid():
    #         print('> snippet is_valid')
    #         snippet = serializer.save()
    #         for d in details:
    #             d['snippet'] = snippet.id
    #
    #         print(details)
    #         serializer_details = SnippetDetailSerializer(data=details, many=True)
    #
    #         if serializer_details.is_valid():
    #             print('> snippet details is_valid')
    #             serializer_details.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         else:
    #             print('> snippet details is_not_valid')
    #             return Response(
    #                 serializer_details.errors,
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )
    #     else:
    #         print('> snippet is_not_valid')
    #         print(serializer.data)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def perform_create(self, serializer):
    #     print('> perform_create')
    #     # print(serializer.data) # This, hasn't the ID
    #     objeto = serializer.save()
    #     print('>'*20)
    #     print(serializer.data)
    #
    #     print(objeto.id) # This, has the ID
