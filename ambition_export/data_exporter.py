import os

from django.apps import apps as django_apps
from edc_pdutils import CsvModelExporter

CSV = 'csv'


EXPORT_FORMATS = (
    (CSV, 'CSV'),
)


class DataExporterError(Exception):
    pass


class DataExporter:

    csv_exporter_cls = CsvModelExporter

    def __init__(self, model=None, timestamp=None, folder=None, decrypt=None,
                 export_format=None):
        self.model_cls = django_apps.get_model(model)
        filename = ('_'.join(
            self.model_cls._meta.label_lower.split('.') + [timestamp])) + '.csv'
        self.filename = os.path.join(folder, filename)
        if export_format == CSV:
            csv_exporter = self.csv_exporter_cls(
                model=self.model_cls._meta.label_lower,
                export_folder=folder,
                decrypt=decrypt)
            self.filename = csv_exporter.to_csv()
        else:
            raise DataExporterError(
                f'Invalid format specified. Got \'{export_format}\'')
