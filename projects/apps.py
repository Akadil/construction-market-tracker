from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'

    # def ready(self):
        # from projects.management.commands.feed_database import Command as InitDataCommand
        # InitDataCommand().handle()