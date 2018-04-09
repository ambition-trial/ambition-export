import os

from django.apps import apps as django_apps
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel

from ..choices import EXPORT_FORMATS
from ..constants import CSV


class DataRequest(BaseUuidModel):

    requested = models.TextField()

    archive_filename = models.CharField(max_length=200, null=True)

    decrypt = models.BooleanField(default=False)

    export_format = models.CharField(
        max_length=25,
        choices=EXPORT_FORMATS,
        default=CSV)

    exported = models.BooleanField(default=False)

    exported_datetime = models.DateTimeField(null=True)

    history = HistoricalRecords()

    def __str__(self):
        return os.path.basename(self.archive_filename)

    @property
    def requested_as_list(self):
        """Returns `requested` as a list.

        Validates each item to be a model name.
        """
        requested = self.requested.split('\n')
        requested = [x.strip() for x in requested if x.strip()]
        for model in requested:
            django_apps.get_model(model)
        return requested
