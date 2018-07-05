import os
import shutil

from django.contrib.auth.models import User
from edc_pdutils import ArchiveExporter
from edc_registration.models import RegisteredSubject
from django.test import TestCase, tag
from django.test.utils import override_settings
from tempfile import mkdtemp

# from ..crf_dialect import CrfDialect
# from ..df_handlers import CrfDfHandler


@override_settings(EXPORT_FOLDER=mkdtemp())
class TestExport(TestCase):

    def setUp(self):

        User.objects.create(username='erikvw')
        RegisteredSubject.objects.create(subject_identifier='12345')

        models = [
            'auth.user',
            'edc_registration.registeredsubject']
        exporter = ArchiveExporter()
        self.history = exporter.export_to_archive(
            models=models,
            user='erikvw')

    def test_request_archive(self):

        folder = mkdtemp()
        shutil.unpack_archive(
            self.history.archive_filename, folder, 'zip')
        filenames = os.listdir(folder)
        self.assertGreater(
            len([f for f in filenames]), 0)

    def test_request_archive_filename_exists(self):
        filename = self.history.archive_filename
        self.assertIsNotNone(filename)
        self.assertTrue(
            os.path.exists(filename),
            msg=f'file \'{filename}\' does not exist')

#     def test_crf_dialect(self):
#         handler = CrfDfHandler()
#         pprint(handler.__dict__)
