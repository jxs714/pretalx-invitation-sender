from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from pretalx.common.mixins.views import PermissionRequired
from pretalx.mail.models import MailTemplate, QueuedMail

from .forms import InviteForm

class InviteView(PermissionRequired, FormView):
    form_class = InviteForm
    template_name = "pretalx_invitation_sender/invite_form.html"
    permission_required = "orga.send_mails"  # This ensures only organizers can access

    def get_permission_object(self):
        return self.request.event

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["event"] = self.request.event
        return kwargs

    def form_valid(self, form):
        event = self.request.event
        template_pk = form.cleaned_data["template"]
        template = MailTemplate.objects.get(pk=template_pk, event=event)
        locale = event.locale

        # Basic context for the email (e.g., event name and CFP link for submissions)
        context = {
            "event": event,
            "cfp_url": event.cfp.urls.base,
        }

        subject = template.render_subject(context, locale)
        text = template.render_text(context, locale)
        html = (
            template.render_html(context, locale)
            if event.settings.mail_use_html
            else None
        )

        to_str = form.cleaned_data["to"]
        bcc_str = form.cleaned_data["bcc"]
        to_list = [e.strip() for e in to_str.split(",") if e.strip()]
        bcc_list = [e.strip() for e in bcc_str.split(",") if e.strip()]

        if not to_list and not bcc_list:
            messages.error(self.request, _("No email addresses provided."))
            return self.get(self.request, *self.args, **self.kwargs)

        # Set TO as the first visible recipient (or event email if none), CC the rest of TO
        to = to_list[0] if to_list else event.email
        cc = to_list[1:] if to_list else []

        # Include any CC/BCC from the template itself
        template_cc = [e.strip() for e in (template.cc or "").split(",") if e.strip()]
        template_bcc = [e.strip() for e in (template.bcc or "").split(",") if e.strip()]
        cc += template_cc
        bcc = bcc_list + template_bcc

        reply_to = template.reply_to or event.email

        mail = QueuedMail(
            event=event,
            to=to,
            reply_to=reply_to,
            cc=cc,
            bcc=bcc,
            subject=subject,
            text=text,
            html=html,
        )
        mail.send()

        total_recipients = len(to_list) + len(bcc_list)
        messages.success(
            self.request, _(f"Email queued for sending to {total_recipient} recipients.")
        )
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path
