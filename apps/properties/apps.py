from django.apps import AppConfig

class PropertiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.properties' # Must have 'apps.' prefix
    label = 'properties'      # Explicit label helps tests find it
