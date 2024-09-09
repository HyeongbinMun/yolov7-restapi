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
    # threshold = serializers.FloatField(write_only=True)

    class Meta:
        model = ImageModel
        fields = ('token', 'image', 'conf_threshold', 'uploaded_date', 'updated_date', 'result_images', 'result')
        read_only_fields = ('token', 'conf_threshold', 'uploaded_date', 'updated_date', 'result_images', 'result')
