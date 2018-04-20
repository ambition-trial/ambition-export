import os
import shutil

from django.conf import settings
from edc_base.utils import get_utcnow
from edc_pdutils import CsvModelExporter
from tempfile import mkdtemp

from .constants import CSV


class DataExporterError(Exception):
    pass


def export_to_archive(data_request=None, export_folder=None, **kwargs):
    exported = []
    tmp_folder = mkdtemp()
    export_folder = export_folder or settings.EXPORT_FOLDER

    if data_request.export_format == CSV:
        for name in data_request.requested_as_list:
            csv_exporter = CsvModelExporter(
                model=name,
                export_folder=tmp_folder,
                decrypt=data_request.decrypt, **kwargs)
            exported.append(csv_exporter.to_csv())
    else:
        raise DataExporterError(
            f'Invalid format specified. Got \'{data_request.export_format}\'')
    if exported:
        user = data_request.user_modified or data_request.user_created or 'unknown_user'
        data_request.exported_datetime = get_utcnow()
        formatted_date = data_request.exported_datetime.strftime(
            '%Y%m%d%H%M%S')
        data_request.archive_filename = shutil.make_archive(
            os.path.join(export_folder, f'{user}_{formatted_date}'), 'zip', tmp_folder)
        data_request.exported = True
        data_request.save()
    return data_request
