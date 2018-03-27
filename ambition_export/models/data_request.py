import os
import shutil

from django.conf import settings
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from tempfile import mkdtemp

from ..data_exporter import DataExporter, EXPORT_FORMATS, CSV


app_labels = [app_label.split('.')[0] for app_label in settings.INSTALLED_APPS]

APP_LABELS = (
    ((x, x) for x in app_labels),
)


class DataRequest(BaseUuidModel):

    data_exporter_cls = DataExporter

    requested = models.TextField()

    archive_filename = models.CharField(max_length=200, null=True)

    decrypt = models.BooleanField(default=False)

    export_format = models.CharField(
        max_length=25,
        choices=EXPORT_FORMATS,
        default=CSV)

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        exported = []
        timestamp = self.modified.strftime('%Y%m%d%H%M%S')
        folder = mkdtemp()
        for name in self.requested_as_list:
            exported.append(self.data_exporter_cls(
                model=name, timestamp=timestamp, folder=folder,
                decrypt=self.decrypt,
                export_format=self.export_format))
        if exported:
            user = self.user_modified or self.user_created
            self.archive_filename = shutil.make_archive(
                os.path.join(settings.EXPORT_FOLDER, f'{user}_{timestamp}'),
                'zip', folder)
        super().save(*args, **kwargs)

    @property
    def requested_as_list(self):
        requested = self.requested.split('\n')
        return [x.strip() for x in requested if x.strip()]
