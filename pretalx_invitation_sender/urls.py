from django.urls import path

from .views import InviteView

urlpatterns = [
    path("invites/", InviteView.as_view(), name="send"),
]
