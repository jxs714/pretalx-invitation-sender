from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class InvitationSenderConfig(AppConfig):
    name = "pretalx_invitation_sender"
    verbose_name = _("Invitation Sender")

    class PretalxPluginMeta:
        name = _("Invitation Sender")
        author = "Your Name"
        version = "0.1.0"
        visible = True
        description = _("Allows sending invite emails to multiple addresses using existing templates.")
        category = "CUSTOMIZATION"

    def ready(self):
        from . import signals  # NOQA
