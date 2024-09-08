# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView

from WebAnalyzer.models import ImageModel, ResultImage
from WebAnalyzer.serializers import ImageSerializer
from rest_framework import viewsets
from rest_framework.response import Response


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.order_by('-token')

        token = self.request.query_params.get('token', None)
        if token is not None:
            queryset = queryset.filter(token=token)

        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        result_images = ResultImage.objects.filter(image_model=instance)
        result_image_urls = [request.build_absolute_uri(img.image.url) for img in result_images]

        return Response({
            'token': instance.token,
            'image': request.build_absolute_uri(instance.image.url),
            'result_images': result_image_urls
        })


class ImageComparisonView(TemplateView):
    template_name = 'viewimages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = ImageModel.objects.all()
        return context
