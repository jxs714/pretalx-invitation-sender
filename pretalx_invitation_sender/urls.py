from django.urls import path

from .views import InvitationView

# This line is the critical fix. It explicitly creates the namespace
# that the error message says is missing.
app_name = "pretalx_invitation_sender"

urlpatterns = [
    path(
        "",
        InvitationView.as_view(),
        name="send",
    ),
]
