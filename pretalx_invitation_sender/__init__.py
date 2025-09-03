from django.apps import AppConfig
from django.utils.translation import gettext_lazy

from . import __version__


class PluginApp(AppConfig):
    name = "pretalx_invitation_sender"
    verbose_name = "Pretalx Invitation Sender"

    class PretalxPluginMeta:
        name = gettext_lazy("Pretalx Invitation Sender")
        author = "Your Name"
        description = gettext_lazy(
            "A plugin to send invitation emails to users who have not yet registered."
        )
        visible = True
        version = __version__
        category = "FEATURE"

    def ready(self):
        from . import signals  # NOQA