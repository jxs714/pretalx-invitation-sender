from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from .__version__ import __version__


class PretalxPluginMeta:
    name = _("Invitation Sender")
    author = "Your Name"
    description = _("A plugin to send talk submission invitations to external users.")
    visible = True
    version = __version__
    category = "FEATURE"


class PluginApp(AppConfig):
    name = "pretalx_invitation_sender"
    verbose_name = "A plugin to send talk submission invitations to external users."

    def ready(self):
        from . import signals
