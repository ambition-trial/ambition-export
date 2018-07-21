from edc_pdutils import CrfDfHandler as BaseCrfDfHandler
from edc_pdutils import NonCrfDfHandler as BaseNonCrfDfHandler
from edc_pdutils import SYSTEM_COLUMNS

from .column_handlers import ColumnHandler
from .crf_dialect import CrfDialect


class CrfDfHandler(BaseCrfDfHandler):

    system_columns = SYSTEM_COLUMNS
    column_handler_cls = ColumnHandler
    na_value = '.'

    crf_dialect_cls = CrfDialect
    visit_column = 'subject_visit_id'
    visit_tbl = 'ambition_subject_subjectvisit'
    enrollment_tbl = 'ambition_screening_subjectscreening'
#     hiv_status_tbl = 'td_maternal_rapidtestresult'
    rando_tbl = 'ambition_rando_randomizationlist'
    sort_by = ['subject_identifier', 'visit_datetime']


class NonCrfDfHandler(BaseNonCrfDfHandler):

    system_columns = SYSTEM_COLUMNS
    column_handler_cls = ColumnHandler
    na_value = '.'
