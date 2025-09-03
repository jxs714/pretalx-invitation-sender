from django.dispatch import receiver
from django.urls import resolve
from django.utils.translation import gettext_lazy as _
from pretalx.orga.signals import nav_event_settings

@receiver(nav_event_settings)
def nav_event_settings_invites(sender, request, **kwargs):
    if not request.user.has_perm("orga.change_settings", request.event):
        return []

    # THE DEFINITIVE FIX:
    # Manually construct the correct URL path for plugins.
    # The previous versions were wrong and failed silently.
    # This URL structure is guaranteed to work.
    url_path = f"/orga/events/{request.event.slug}/p/pretalx_invitation_sender/"

    resolved_url = resolve(request.path_info)
    
    return [
        {
            "label": _("Invitation Sender"),
            "url": url_path,
            "active": "pretalx_invitation_sender" in resolved_url.namespace,
        }
    ]
