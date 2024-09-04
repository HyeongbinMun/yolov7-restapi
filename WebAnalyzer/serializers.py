# -*- coding: utf-8 -*-
from rest_framework import serializers
from WebAnalyzer.models import *


class ImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ImageModel
        fields = ('token', 'image', 'uploaded_date', 'updated_date', 'result_image', 'result')
        read_only_fields = ('token', 'uploaded_date', 'updated_date', 'result_image', 'result')