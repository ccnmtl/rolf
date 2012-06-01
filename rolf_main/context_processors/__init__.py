from django.conf import settings


def wind_settings(request):
    if hasattr(settings, 'WIND_BASE'):
        return {'wind_base': settings.WIND_BASE,
                'wind_service': settings.WIND_SERVICE}
    else:
        return {'wind_base': None}
