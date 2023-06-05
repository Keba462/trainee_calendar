from django.apps import AppConfig as DjangoApponfig


class AppConfig(DjangoApponfig):
    name = 'trainee_calendar'
    app_name = 'trainee_calendar'
    app_label = 'trainee_calendar'
    verbose_name = 'Trainee Calendar'
    extra_assignee_choices = ()
    assignable_users_group = 'assignable users'