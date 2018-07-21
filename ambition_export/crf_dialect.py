from edc_pdutils.dialects.crf_dialect import CrfDialect as BaseCrfDialect


class CrfDialect(BaseCrfDialect):

    @property
    def select_visit_and_related(self):
        """Returns an SQL statement that joins visit,
        appt, and registered_subject.
        """
        sql = (
            'SELECT R.subject_identifier, R.screening_identifier, R.sid, R.dob, '
            'R.gender, R.subject_type, R.sid, '
            'V.report_datetime as visit_datetime, A.appt_status, '
            'A.visit_code, A.timepoint, V.reason, '
            'A.appt_datetime, A.timepoint_datetime,  '
            'R.screening_age_in_years, R.registration_status, R.registration_datetime, '
            'R.randomization_datetime, V.survival_status, V.last_alive_date, '
            f'V.id as {self.obj.visit_column} '
            f'from {self.obj.appointment_tbl} as A '
            f'LEFT JOIN {self.obj.visit_tbl} as V on A.id=V.appointment_id '
            f'LEFT JOIN {self.obj.registered_subject_tbl} as R '
            'on A.subject_identifier=R.subject_identifier ')
        return sql, None
