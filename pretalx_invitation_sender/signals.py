from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _
from pretalx.orga.signals import nav_event_settings


@receiver(nav_event_settings)
def nav_event_settings_invites(sender, request, **kwargs):
    """
    Adds a navigation item to the event settings sidebar for sending invitations.
    """
    url = reverse(
        "plugins:pretalx_invitation_sender:send",
        kwargs={"event": request.event.slug},
    )
    # Check if the current URL matches the plugin's URL to set the 'active' state
    is_active = request.resolver_match and request.resolver_match.url_name == "send"

    return [
        {
            "label": _("Send Invites"),
            "url": url,
            "active": is_active,
            "icon": "paper-plane",
        }
    ]