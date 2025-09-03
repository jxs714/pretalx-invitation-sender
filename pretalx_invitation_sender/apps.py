from django.apps import AppConfig


class InvitationSenderAppConfig(AppConfig):
    name = "pretalx_invitation_sender"
    label = "pretalx_invitation_sender"
    verbose_name = "Pretalx Invitation Sender"

    def ready(self):
        from . import signals  # NOQA

default_app_config = "pretalx_invitation_sender.apps.InvitationSenderAppConfig"