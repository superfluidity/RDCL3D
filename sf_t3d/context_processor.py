from django.conf import settings  # import the settings file


def conf_constants(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SHORT_SITE_NAME': settings.SHORT_SITE_NAME,
        'VERSION': settings.VERSION,
    }