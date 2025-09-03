from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from pretalx.orga.signals import nav_event

@receiver(nav_event)
def add_nav_item(sender, request, **kwargs):
    url = reverse(
        "plugins:pretalx_invitation_sender:send",
        kwargs={"event": sender.slug},
    )
    return [
        {
            "label": _("Send Invites"),
            "url": url,
            "active": request.path == url,
            "icon": "envelope",
        }
    ]
