from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from .__version__ import __version__


class PluginApp(AppConfig):
    name = "pretalx_invitation_sender"
    verbose_name = "A plugin to send talk submission invitations to external users."

    class PretalxPluginMeta:
        name = _("Invitation Sender")
        author = "You"
        description = _("A plugin to send talk submission invitations to external users.")
        visible = True
        version = __version__
        category = "FEATURE"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from . import signals

    def ready(self, *args, **kwargs):
        super().ready(*args, **kwargs)
