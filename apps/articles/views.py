from operator import itemgetter
from itertools import groupby

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *

from .models import Article, Category


class ArticlePagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 1000


class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Article.objects.all()
    pagination_class = ArticlePagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('category__name',)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        else:
            return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArticleRetrieveSerializer
        elif self.action == 'create':
            return ArticleCreateSerializer
        else:
            return ArticleSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view += 1
        instance.save()
        serializer = self.get_serializer(instance)
        serializer = serializer.data
        serializer['comments'] = [comment for comment in serializer['comments'] if comment['parent'] is None]
        return Response(serializer)


class CategoryViewSet(ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        else:
            return CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update']:
            return [IsAdminUser()]
        else:
            return []


class ArchiveViewSet(ListModelMixin, GenericViewSet):
    serializer_class = ArticleArchiveSerializer

    def list(self, request, *args, **kwargs):
        queryset = Article.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        data = groupby(serializer.data, itemgetter('created_time'))
        archive_data = dict([(key, list(group)) for key, group in data])
        return Response(archive_data)
