"""
    Module name :- apps
    Classes :- AccountConfig
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Path of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
