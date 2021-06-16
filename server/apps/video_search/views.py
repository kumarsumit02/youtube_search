from django.shortcuts import render

# from rest_framework import viewsets
from rest_framework import generics
# from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import VideoSerializer
from .models import Videos


class VideoDataApiView(generics.ListAPIView):

    serializer_class = VideoSerializer
    pagination_class = LimitOffsetPagination
    queryset = Videos.objects.all().order_by('-published_at')

class VideoSearchApiView(generics.ListAPIView):

    serializer_class = VideoSerializer
    pagination_class = LimitOffsetPagination
    queryset = Videos.objects.all().order_by('-published_at')
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['title']
