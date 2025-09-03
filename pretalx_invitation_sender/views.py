from django.contrib import messages
from django.views.generic.edit import FormView
from django.utils.translation import gettext_lazy as _
from pretalx.common.mixins.views import EventPermissionRequired
from .forms import InvitationForm


class InvitationView(EventPermissionRequired, FormView):
    """
    This view provides the page for organizers to send new user invitations.
    """

    permission_required = "orga.change_settings"
    template_name = "pretalx_invitation_sender/send_form.html"
    form_class = InvitationForm

    def get_success_url(self):
        """
        Redirects back to the same page on successful form submission.
        """
        return self.request.path

    def get_form_kwargs(self):
        """
        Passes the current event to the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs["event"] = self.request.event
        return kwargs

    def form_valid(self, form):
        """
        Processes the valid form data, creates QueuedMail objects for each
        recipient, and places them in the outbox.
        """
        template = form.cleaned_data["template"]
        recipients = form.cleaned_data["recipients"]
        bcc = form.cleaned_data["bcc"]
        event = self.request.event
        mails_created_count = 0

        for recipient in recipients:
            # The to_mail method prepares an email from a template.
            # commit=True saves it to the database (in the outbox).
            # The context is empty as we have no user-specific data yet.
            mail = template.to_mail(
                user=None,  # No specific user context for external invites
                event=event,
                context={},
                commit=True,
                full_submission_content=False,
            )
            mail.to = recipient
            mail.bcc = ", ".join(bcc) if bcc else None
            mail.save()
            mails_created_count += 1

        if mails_created_count > 0:
            messages.success(
                self.request,
                _(
                    f"{mails_created_count} invitation emails have been created and placed in the outbox for review."
                ),
            )
        else:
            messages.warning(self.request, _("No emails were created."))

        return super().form_valid(form)