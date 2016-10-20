from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        # Register signals listeners
        import users.signals

        # Register activity stream listeners
        from actstream import registry
        registry.register(self.get_model(model_name='UserProfile'))
