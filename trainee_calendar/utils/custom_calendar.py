from edc_appointment.models import Appointment
from trainee_calendar.utils.appointment_html_builder import AppointmentHtmlBuilder
from datetime import datetime
from django.db.models import Q
from calendar import HTMLCalendar

class CustomCalendar(HTMLCalendar):

    def __init__(self, year=None, month=None, request=None):
        self.year = year
        self.month = month
        self.filter = request.session.get('filter', None)
        self.search_term = request.session.get('search_term', None)
        self.request = request
        super(CustomCalendar, self).__init__()

    
    def formatday(self, day, events):

        events_per_day = []
        for event in events:
            if isinstance(event, Appointment):
                if event.appt_datetime.day == day:
                    events_per_day.append(event)

        d = ''
        appointment_counter = 0
    

        for event in events_per_day:
            if  isinstance(event, Appointment):
                d += AppointmentHtmlBuilder(event, self.request).view_build()
                appointment_counter += 1
        if day != 0:
            today_day = datetime.today().day
            return f'''\
                <td>
                    <span class='date {"today" if day == today_day else ""}'>{day}</span>
                    <ul style="height: 200px; overflow: scroll;"> {d} </ul>
                    <p align="center" style="padding-top: 2px; margin-botton: 1 px; border-top: 1px solid #17a2b8;" >A ({appointment_counter})</p>
                </td>
                '''
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):

        events = list()

        q_objects = Q()

        if self.search_term:
            q_objects = Q(subject_identifier__icontains=self.search_term)

        else :
            subject_appointments = Appointment.objects.filter(
                ~Q(user_modified='trainee') & q_objects,
                appt_datetime__year=self.year,
                appt_datetime__month=self.month)
            events = list(subject_appointments)

        events = list(filter(lambda e: 'comment' not in getattr(e, 'title', '').lower(),
                             events))
        
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal
    