from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class InvitationSenderConfig(AppConfig):
    name = "pretalx_invitation_sender"
    verbose_name = _("Invitation Sender")

    def ready(self):
        from . import signals  # NOQA
