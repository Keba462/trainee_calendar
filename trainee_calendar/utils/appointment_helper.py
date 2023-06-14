from edc_appointment.models import Appointment

class AppointmentHelper:

    @classmethod
    def all_search_appointments(cls, subject_identifier, type):

        results = []

        if subject_identifier:

            if type == 'subject':
                subject_appointments = Appointment.objects.filter(
                    subject_identifier__icontains=subject_identifier)
                results.extend(subject_appointments)


            elif type == 'all':

                subject_appointments = Appointment.objects.filter(
                    subject_identifier__icontains=subject_identifier)
                
            results.extend(subject_appointments)
            
        return results