from django.apps import AppConfig


class OrderConfig(AppConfig):
    name = 'order'

    def ready(self):
        # Register activity stream listeners
        from actstream import registry
        registry.register(self.get_model(model_name='Order'))