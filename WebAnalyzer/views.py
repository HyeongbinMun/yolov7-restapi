# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView

from WebAnalyzer.models import ImageModel, ResultImage
from WebAnalyzer.serializers import ImageSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer

    def get_queryset(self):
        queryset = self.queryset.order_by('-token')
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

    def create(self, request, *args, **kwargs):
        image = request.FILES.get('image')
        if not image:
            return Response({'error': 'Image file is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conf_threshold = float(request.data.get('conf_thresh', 0.1))
        except ValueError:
            return Response({'error': 'Invalid conf_thresh value'}, status=status.HTTP_400_BAD_REQUEST)

        image_instance = ImageModel(image=image, conf_threshold=conf_threshold)
        image_instance.save()

        return Response({
            'message': 'Image uploaded and processing started!',
            'image_token': image_instance.token,
            'conf_thresh': conf_threshold,
        }, status=status.HTTP_201_CREATED)

class ImageComparisonView(TemplateView):
    template_name = 'viewimages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = ImageModel.objects.all()
        return context
