from django.views import generic
from edc_appointment.models import Appointment
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from trainee_calendar.utils.appointment_helper import AppointmentHelper
from trainee_calendar.utils.custom_calendar import CustomCalendar
from trainee_calendar.utils.date_helper import DateHelper
from django.utils.safestring import mark_safe

class HomeView(NavbarViewMixin, EdcBaseViewMixin, generic.ListView):

    navbar_name = 'trainee_calendar'
    model = Appointment
    navbar_selected_item ='calendar'
    template_name ='trainee_calendar/home.html'


    def get_context_data (self,**kwargs):
        context = super().get_context_data(**kwargs)
    
        month = self.request.GET.get('month', None)

        # use today's date for the calendar
        d = DateHelper.get_date(month)

        search_filter = self.request.GET.get('filter', None)
        search_term = self.request.GET.get('search_term', None)
        if search_filter:
            self.request.session['filter'] = search_filter
        elif search_filter == 'all':
            del self.request.session['filter']

        if search_filter:
            search_term = search_term.strip()
            self.request.session['search_term'] = search_term.strip()
        else:
            if self.request.session.get('search_term', None):
                del self.request.session['search_term']

        appointment_search_results = AppointmentHelper.all_search_appointments(subject_identifier=search_term,
                                                                               type=search_filter)

         # Instantiate our calendar class with today's year and date
        cal = CustomCalendar(d.year, d.month, self.request)

        # Call the formatmonth method, which returns our calendar as a table

        html_cal = cal.formatmonth(withyear=True)
            
        
        context.update(
        
            prev_month=DateHelper.prev_month(d),
            next_month=DateHelper.next_month(d),
            calendar=mark_safe(html_cal),
            filter=search_filter,
            search_term=search_term,
            appointment_search_results=appointment_search_results,
        )
        return context