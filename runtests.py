#!/usr/bin/env python
import django
import logging
import os
import sys

from django.conf import settings
from django.test.runner import DiscoverRunner
from edc_test_utils import DefaultTestSettings
from os.path import abspath, dirname, join


app_name = 'ambition_export'
base_dir = dirname(abspath(__file__))

DEFAULT_SETTINGS = DefaultTestSettings(
    calling_file=__file__,
    BASE_DIR=base_dir,
    APP_NAME=app_name,
    ETC_DIR=os.path.join(base_dir, app_name, "tests", "etc"),
    SUBJECT_VISIT_MODEL="ambition_subject.subjectvisit",
    EDC_BOOTSTRAP=3,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    EMAIL_CONTACTS={
        "data_request": "someone@example.com",
        "data_manager": "someone@example.com",
        "tmg": "someone@example.com",
    },
    EMAIL_ENABLED=True,
    HOLIDAY_FILE=join(base_dir, app_name, "tests", "holidays.csv"),
    LIVE_SYSTEM=False,
    RANDOMIZATION_LIST_PATH=join(
        base_dir, app_name, "tests", "test_randomization_list.csv"),
    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_crypto_fields.apps.AppConfig',
        'django_revision.apps.AppConfig',
        'edc_registration.apps.AppConfig',
        'ambition_export.apps.AppConfig',
    ],
    add_dashboard_middleware=True,
    add_lab_dashboard_middleware=True,
    # use_test_urls=True,
).settings


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    tags = [t.split('=')[1] for t in sys.argv if t.startswith('--tag')]
    failures = DiscoverRunner(failfast=True, tags=tags).run_tests(
        [f'{app_name}.tests'])
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()
