from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _

from pretalx.orga.signals import nav_event_settings

# A helper function that is robust against different URL setups
def resolve_or_reverse(request, url_name, **kwargs):
    try:
        return reverse(url_name, kwargs=kwargs)
    except Exception:
        return f"/orga/event/{request.event.slug}/{url_name.split(':')[-1]}/"


@receiver(nav_event_settings)
def nav_event_settings_invites(sender, request, **kwargs):
    # This function is called by Pretalx to build the settings navigation
    if not request.user.has_perm("orga.change_settings", request.event):
        return []
    
    # Get the current path to check if our menu item should be "active"
    url = resolve(request.path_info)
    
    # This is the menu item that will be displayed
    return [
        {
            "label": _("Send Invites"),
            "url": resolve_or_reverse(request, "plugins:pretalx_invitation_sender:send", event=request.event.slug),
            "active": url.namespace == "plugins:pretalx_invitation_sender" and url.url_name == "send",
        }
    ]
