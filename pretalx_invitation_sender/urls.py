from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.InvitationView.as_view(),
        name="send",
    ),
]
