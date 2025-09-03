from django.dispatch import receiver
from django.urls import resolve
from django.utils.translation import gettext_lazy as _
from pretalx.orga.signals import nav_event_settings

@receiver(nav_event_settings)
def nav_event_settings_invites(sender, request, **kwargs):
    if not request.user.has_perm("orga.change_settings", request.event):
        return []
    
    # Manually construct the URL to bypass the failing reverse() lookup
    url_path = f"/orga/events/{request.event.slug}/settings/p/pretalx_invitation_sender/"
    
    # Resolve the current path to check if our menu item should be "active"
    resolved_url = resolve(request.path_info)
    
    return [
        {
            "label": _("Send Invites"),
            "url": url_path,
            "active": "pretalx_invitation_sender" in resolved_url.namespace,
        }
    ]
