from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _

from pretalx.orga.signals import nav_event_settings

@receiver(nav_event_settings)
def nav_event_settings_invites(sender, request, **kwargs):
    if not request.user.has_perm("orga.change_settings", request.event):
        return []

    url = resolve(request.path_info)
    
    return [
        {
            "label": _("Send Invites"),
            "url": reverse("plugins:pretalx_invitation_sender:send", kwargs={"event": request.event.slug}),
            "active": url.namespace == "plugins:pretalx_invitation_sender" and url.url_name == "send",
        }
    ]
