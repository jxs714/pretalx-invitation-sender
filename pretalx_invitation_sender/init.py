from .apps import InvitationSenderConfig

class PretalxPluginMeta(InvitationSenderConfig):
    name = _("Invitation Sender")
    author = "Your Name"
    version = "0.1.0"
    visible = True
    description = _("Allows sending invite emails to multiple addresses using existing templates.")
    category = "CUSTOMIZATION"
