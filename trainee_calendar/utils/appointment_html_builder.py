from edc_appointment.models import Appointment
from django.apps import apps as django_apps
from trainee_dashboard.model_wrappers.subject_locator_model_wrapper import SubjectLocatorModelWrapper
from edc_appointment.choices import (
    NEW_APPT,
    IN_PROGRESS_APPT,
    INCOMPLETE_APPT,
    COMPLETE_APPT,
    CANCELLED_APPT
)
from django.template.loader import render_to_string

class AppointmentHtmlBuilder:
    subject_locator_model = 'trainee_subject.subjectlocator'

    def __init__(self, appointment: Appointment, request) -> None:
        self._appointment = appointment
        self._subject_identifier = self._appointment.subject_identifier
        self.request = request

    @property
    def subject_locator_cls(self):
        return django_apps.get_model(self.subject_locator_model)

    @property
    def model_obj(self):
        return self._appointment
    
    @property
    def html_wrapped_status(self):
        """
        NEW_APPT,
        IN_PROGRESS_APPT,
        INCOMPLETE_APPT,
        COMPLETE_APPT,
        CANCELLED_APPT⚠️⚠️
        """
        status = self._appointment.appt_status
        if status == NEW_APPT:
            return f'''\
                <span style="color: orange;" title="New Appointment">{self.status} </span>
                '''
        elif status == IN_PROGRESS_APPT:
            return f'''\
                <span style="color: blue;" class="blink-one" title="Inprogress Appointment">{self.status}</span>
                '''
        elif status == COMPLETE_APPT:
            return f'''\
                <span style="color: green;" title="Complete Appointment">{self.status} ✅</span>
                '''
        elif status == INCOMPLETE_APPT:
            return f'''\
                <span style="color: green;" title="Incomplete Appointment">{self.status} ⚠️</span>
                '''
        elif (status == CANCELLED_APPT):
            return f'''\
                <span style="color: red;" title="Cancelled Appointment">{self.status}</span>
                '''

    @property
    def status(self):
        return self._appointment.appt_status.replace("_", " ").title()
    

    @property
    def subject_identifier(self):
        return self._subject_identifier

    @property
    def visit_code(self):
        return self._appointment.visit_code

    @property
    def previous_appointments(self):
        return self._appointment.history.all()

    @property
    def resceduled_appointments_count(self):
        prev_appt = self.previous_appointments.values_list(
            'appt_datetime__date', flat=True)
        prev_appt_set = set(prev_appt)
        return len(prev_appt_set) - 1

    @property
    def last_appointment(self):
        appt = self.previous_appointments.exclude(
            timepoint_datetime__date=self._appointment.appt_datetime.date())

        if appt:
            return appt.last().appt_datetime.date()
        else:
            return None
        
    def _html(self, dashboard_type):
        view_locator_href = None
        if self.wrapped_locator_obj:
            view_locator_href = self.wrapped_locator_obj.href
        icon = None
        if 'quart' in self._appointment.schedule_name:
            icon = '📞'
        else:
            icon = '👩'
        view = render_to_string('trainee_calendar/appointment_template.html', {
            'dashboard_type': dashboard_type,
            'subject_identifier': self.subject_identifier,
            'visit_code': self.visit_code,
            'status': self.status,
            'resceduled_appointments_count': self.resceduled_appointments_count,
            'icon': icon,
            'date': self._appointment.appt_datetime.date().isoformat(),
            'is_not_sec': 'sec' not in self._appointment.schedule_name,
            'view_locator_href': view_locator_href
        }, request=self.request)

        return view

    def view_build(self):
            return self._html('subject_dashboard')

    @property
    def locator_obj(self):
        try:
            locator_obj = self.subject_locator_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except self.subject_locator_cls.DoesNotExist:
            return None
        else:
            return locator_obj

    @property
    def wrapped_locator_obj(self):
        return SubjectLocatorModelWrapper(self.locator_obj) if self.locator_obj else None

