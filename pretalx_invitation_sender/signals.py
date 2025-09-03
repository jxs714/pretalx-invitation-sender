from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _
from pretalx.orga.signals import nav_event_settings

@receiver(nav_event_settings)
def nav_event_settings_invites(sender, request, **kwargs):
    if not request.user.has_perm("orga.change_settings", request.event):
        return []

    # Now that urls.py is fixed, this reverse() call will succeed.
    url_path = reverse(
        "plugins:pretalx_invitation_sender:send",
        kwargs={"event": request.event.slug},
    )

    resolved_url = resolve(request.path_info)
    
    return [
        {
            "label": _("Invitation Sender"),
            "url": url_path,
            "active": "pretalx_invitation_sender" in resolved_url.namespace,
        }
    ]
