from django.apps import AppConfig


class AuthorsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authors"

    def ready(self, *args, **kwargs) -> None:
        import authors.signals
        super_ready = super(*args, **kwargs).ready()
        return super_ready
