import os
import shutil

from django.apps import apps as django_apps
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_pdutils import CsvModelExporter
from tempfile import mkdtemp


class DataExporter:

    def __init__(self, model=None, timestamp=None, folder=None):
        self.folder = mkdtemp()
        self.model_cls = django_apps.get_model(model)
        filename = ('_'.join(
            self.model_cls._meta.label_lower.split('.') + [timestamp])) + '.csv'
        self.filename = os.path.join(self.folder, filename)
        exporter = CsvModelExporter(
            model=self.model_cls._meta.label_lower,
            export_folder=folder,
            delimiter='|',
            decrypt=False)
        self.filename = exporter.to_csv()


class DataRequest(BaseUuidModel):

    requested = models.TextField()

    archive_filename = models.CharField(max_length=200, null=True)

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        exported = []
        timestamp = self.modified.strftime('%Y%m%d%H%M%S')
        folder = mkdtemp()
        for name in self.requested_as_list:
            exported.append(DataExporter(
                model=name, timestamp=timestamp, folder=folder))
        if exported:
            user = self.user_modified or self.user_created
            self.archive_filename = shutil.make_archive(
                f'{user}_{timestamp}', 'zip', folder)
        super().save(*args, **kwargs)

    @property
    def requested_as_list(self):
        requested = self.requested.split('\n')
        return [x.strip() for x in requested if x.strip()]
