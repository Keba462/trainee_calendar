from django.contrib.admin import AdminSite as DjangoAdminSite

class AdminSite(DjangoAdminSite):
    site_title = 'Trainee Calendar'
    site_header = 'Trainee Calendar'
    site_url = '/administration'
    index_title = 'Trainee_Calendar'
    enable_nav_sidebar =False


trainee_calendar_admin = AdminSite(name='trainee_calendar_admin')