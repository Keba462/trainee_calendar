from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


trainee_calendar = Navbar(name='trainee_calendar')

no_url_namespace = True if settings.APP_NAME == 'trainee_calendar' else False


trainee_calendar.append_item(
    NavbarItem(
        name='calendar',
        label='Calendar',
        fa_icon='far fa-calendar',
        url_name='trainee_calendar:calendar'))


site_navbars.register(trainee_calendar)