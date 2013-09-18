'''
Configuration from django settings.
'''

from django.conf import settings


def get_config_redirectors():
    # TODO: make this default true
    return getattr(settings, 'CMS_SEOUTILS_REDIRECTORS', False)
