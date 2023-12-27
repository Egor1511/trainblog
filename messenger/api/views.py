from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from main.models import MyBlog, Contact
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import BlogListSerializer, PopularPostsSerializer, ContactSerializer


class BlogViewSet(ListModelMixin, GenericViewSet):
    queryset = MyBlog.objects.all().select_related('category', 'author')
    serializer_class = BlogListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    ordering_fields = ('id', 'title', 'slug', 'time_create',
                       'category', 'read_counter')
    search_fields = ('title', 'subtitle', 'slug', 'description')

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(
            MyBlog.objects.all(),
            pk=pk
        )
        queryset.read_counter += 1
        queryset.save()
        serializer = BlogListSerializer(queryset)
        return Response(serializer.data)

    @action(methods=['GET'],
            detail=False,
            url_path=r'popular',
            url_name='popular')
    def popular(self, request):
        queryset = self.filter_queryset(self.get_queryset()).order_by(
            '-read_counter')[:5]
        serializer = PopularPostsSerializer(queryset, many=True)
        return Response(serializer.data)


class ContactViewSet(CreateModelMixin, GenericViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]
