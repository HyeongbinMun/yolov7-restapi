# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import ast
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from WebAnalyzer.utils import filename
from WebAnalyzer.utils.media import *
from WebAnalyzer.tasks import app
from django.db.models import JSONField


class ResultImage(models.Model):
    image_model = models.ForeignKey('ImageModel', related_name='result_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=filename.default)
    uploaded_date = models.DateTimeField(auto_now_add=True)

class ImageModel(models.Model):
    image = models.ImageField(upload_to=filename.default)
    conf_threshold = models.FloatField(default=0.1)
    token = models.AutoField(primary_key=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    result = JSONField(null=True)

    def save(self, *args, **kwargs):
        super(ImageModel, self).save(*args, **kwargs)

        task_result = app.send_task(
            name='WebAnalyzer.tasks.analyzer_by_image',
            args=[self.image.path, self.conf_threshold],
            exchange='WebAnalyzer',
            routing_key='webanalyzer_tasks',
        )

        result, out_images = task_result.get()
        self.result = ast.literal_eval(str(result))

        for idx, out_image in enumerate(out_images):
            rgb_image = cv2.cvtColor(out_image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_image.astype('uint8'))

            buffer = BytesIO()
            img.save(buffer, format='PNG')
            new_file_name = os.path.basename(self.image.name).split(".")[0] + f"_result_{idx}.png"
            file_len = buffer.tell()
            buffer.seek(0)

            result_image = ResultImage(image_model=self)
            result_image.image.save(
                f"{os.path.basename(self.image.name).split('.')[0]}_result_{idx}.png",
                InMemoryUploadedFile(buffer, 'ImageField', new_file_name, 'image/png', file_len, None),
                save=False
            )
            result_image.save()

        super(ImageModel, self).save()


