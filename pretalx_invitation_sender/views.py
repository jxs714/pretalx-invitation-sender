from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView
from pretalx.common.mixins.views import EventPermissionRequired
from pretalx.mail.models import QueuedMail
from .forms import InvitationForm


class InvitationView(EventPermissionRequired, FormView):
    permission_required = "orga.change_settings"
    template_name = "pretalx_invitation_sender/send_form.html"
    form_class = InvitationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["event"] = self.request.event
        return kwargs

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        template = form.cleaned_data["template"]
        to_recipients = [
            email.strip() for email in form.cleaned_data["to_recipients"].splitlines() if email.strip()
        ]
        bcc_recipients = [
            email.strip() for email in form.cleaned_data["bcc_recipients"].splitlines() if email.strip()
        ]
        total_sent = 0
        for email in to_recipients:
            mail = QueuedMail(
                event=self.request.event, to=email, bcc=", ".join(bcc_recipients),
                reply_to=template.reply_to, subject=template.subject,
                text=template.text, template=template,
            )
            mail.save()
            total_sent += 1
        
        if bcc_recipients and not to_recipients:
            mail = QueuedMail(
                event=self.request.event, to=None, bcc=", ".join(bcc_recipients),
                reply_to=template.reply_to, subject=template.subject,
                text=template.text, template=template,
            )
            mail.save()
            total_sent += 1

        if total_sent > 0:
            messages.success(
                self.request,
                _("%(count)d invitation emails have been placed in the outbox.") % {"count": total_sent},
            )
        else:
            messages.warning(self.request, _("No email addresses were provided."))
        return HttpResponseRedirect(self.get_success_url())
