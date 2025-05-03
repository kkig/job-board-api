from .celery import app as celery_app


# Make sure Celery is loaded when Django starts
__all__ = ('celery_app',)
