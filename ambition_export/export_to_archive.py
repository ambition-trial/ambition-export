import os
import shutil

from django.conf import settings
from edc_base.utils import get_utcnow
from edc_pdutils import CsvModelExporter
from tempfile import mkdtemp

from .constants import CSV


class DataExporterError(Exception):
    pass


def export_to_archive(data_request=None):
    exported = []
    folder = mkdtemp()

    if data_request.export_format == CSV:
        for name in data_request.requested_as_list:
            csv_exporter = CsvModelExporter(
                model=name,
                export_folder=folder,
                decrypt=data_request.decrypt)
            exported.append(csv_exporter.to_csv())
    else:
        raise DataExporterError(
            f'Invalid format specified. Got \'{data_request.export_format}\'')
    if exported:
        user = data_request.user_modified or data_request.user_created
        data_request.exported_datetime = get_utcnow()
        formatted_date = data_request.exported_datetime.strftime(
            '%Y%m%d%H%M%S')
        data_request.archive_filename = shutil.make_archive(
            os.path.join(settings.EXPORT_FOLDER, f'{user}_{formatted_date}'), 'zip', folder)
        data_request.exported = True
        data_request.save()
