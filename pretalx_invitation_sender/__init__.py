from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from .__version__ import __version__


# This class is the Django App definition
class PluginApp(AppConfig):
    name = "pretalx_invitation_sender"
    verbose_name = "A plugin to send talk submission invitations to external users."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from . import signals

    def ready(self, *args, **kwargs):
        super().ready(*args, **kwargs)


# --- FIX ---
# This class MUST be at the top level of the file, not nested.
# This is the metadata that Pretalx reads to display the plugin in the list.
class PretalxPluginMeta:
    name = _("Invitation Sender")
    author = "You"
    description = _("A plugin to send talk submission invitations to external users.")
    visible = True
    version = __version__
    category = "FEATURE"
