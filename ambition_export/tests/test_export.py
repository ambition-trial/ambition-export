import os
import shutil

from django.test import TestCase, tag
from django.test.utils import override_settings
from tempfile import mkdtemp

from ..data_exporter import CSV
from ..models import DataRequest
from django.contrib.auth.models import User
from edc_registration.models import RegisteredSubject


@override_settings(EXPORT_FOLDER=mkdtemp())
class TestExport(TestCase):

    def setUp(self):

        User.objects.create(username='erikvw')
        RegisteredSubject.objects.create(subject_identifier='12345')

        requested = """
        auth.user
        edc_registration.registeredsubject
        """
        self.data_request = DataRequest.objects.create(
            requested=requested,
            export_format=CSV,
            user_created='erikvw')

    def test_request_archive(self):
        folder = mkdtemp()
        shutil.unpack_archive(
            self.data_request.archive_filename, folder, 'zip')
        filenames = os.listdir(folder)
        self.assertGreater(
            len([f for f in filenames]), 0)

    def test_request_archive_filename_exists(self):
        filename = self.data_request.archive_filename
        self.assertIsNotNone(filename)
        self.assertTrue(
            os.path.exists(filename),
            msg=f'file \'{filename}\' does not exist')
