import os, shutil, datetime
from AnalysisEngine.settings import MEDIA_ROOT
from AnalysisEngine.celerys import app
from WebAnalyzer import models
from utils import Logging


@app.task
def delete_old_database(days=1):
    if not os.path.exists(MEDIA_ROOT):
        return 0

    date_today = datetime.date.today()
    date_delta = datetime.timedelta(days)
    date_point = date_today - date_delta

    old_imagemodel_database = models.ImageModel.objects.filter(uploaded_date__lte=date_point)
    old_imagemodel_database_count = old_imagemodel_database.count()

    for record in old_imagemodel_database:
        image_path = os.path.join(MEDIA_ROOT, record.image.name)
        result_image_path = os.path.join(MEDIA_ROOT, record.result_image.name)

        if os.path.exists(image_path):
            os.remove(image_path)
        if os.path.exists(result_image_path):
            os.remove(result_image_path)

    old_imagemodel_database.delete()

    for old_image_dir in os.listdir(MEDIA_ROOT):
        dir_path = os.path.join(MEDIA_ROOT, old_image_dir)
        if not os.listdir(dir_path):
            shutil.rmtree(dir_path)

    print(Logging.i("===================="))
    print(Logging.s(" Delete Old Image"))
    print(Logging.s(" - Date Point: {0}".format(date_point)))
    print(Logging.s("===================="))

    return old_imagemodel_database_count
