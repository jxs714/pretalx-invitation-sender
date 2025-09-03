from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

try:
    from pretalx import __version__ as pretalx_version
except ImportError:
    pretalx_version = "0.0.0"

from .__version__ import __version__


class PretalxPluginMeta:
    name = _("Invitation Sender")
    author = "Your Name"
    description = _("A plugin to send talk submission invitations to external users.")
    visible = True
    version = __version__
    category = "FEATURE"
    compatibility = ">=2025.1.0"


class PluginApp(AppConfig):
    name = "pretalx_invitation_sender"
    verbose_name = "Pretalx Invitation Sender"

    def ready(self):
        from . import signals


default_app_config = "pretalx_invitation_sender.PluginApp"
