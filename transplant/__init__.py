__import__('transplant.settings')
import sys

# Import our defaults, project defaults, and project settings
app_settings = sys.modules['transplant.settings']
default_settings = sys.modules['django.conf.global_settings']
user_settings = sys.modules['django.conf'].settings
        
# Iterate over all uppercase variables in app_settings
for name in dir(app_settings):
    if name.isupper():
        # Add the value to the default settings module
        setattr(default_settings, name, getattr(app_settings, name))
    
        # Add the value to the settings, if not already present
        if not hasattr(user_settings, name):
                setattr(user_settings, name, getattr(default_settings, name))