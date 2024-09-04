# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import ImageModel, ResultImage

class ResultImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultImage
        fields = ('image', 'uploaded_date')
        read_only_fields = ('uploaded_date',)

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    result_images = ResultImageSerializer(many=True, read_only=True)

    class Meta:
        model = ImageModel
        fields = ('token', 'image', 'uploaded_date', 'updated_date', 'result_images', 'result')
        read_only_fields = ('token', 'uploaded_date', 'updated_date', 'result_images', 'result')
