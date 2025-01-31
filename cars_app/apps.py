from django.apps import AppConfig


class CarsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cars_app'


    def ready(self):
        import cars_app  # Замените на имя вашего приложения
