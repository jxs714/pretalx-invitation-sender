from django import forms
from django.utils.translation import gettext_lazy as _
from pretalx.mail.models import MailTemplate


class InvitationForm(forms.Form):
    """
    This form allows organizers to select an email template and enter a list
    of email addresses to send invitations to.
    """

    template = forms.ModelChoiceField(
        queryset=MailTemplate.objects.none(),
        label=_("Email template"),
        help_text=_(
            "Select the email template to use for the invitation. You can create new templates under Settings -> Email."
        ),
    )
    recipients = forms.CharField(
        widget=forms.Textarea,
        label=_("Recipients"),
        help_text=_(
            "Enter one email address per line. These can be for new or existing users."
        ),
        required=True,
    )
    bcc = forms.CharField(
        widget=forms.Textarea,
        label=_("BCC"),
        help_text=_("Enter one email address per line to be blind-copied."),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        """
        Dynamically set the queryset for the template field based on the event.
        """
        self.event = kwargs.pop("event")
        super().__init__(*args, **kwargs)
        self.fields["template"].queryset = self.event.mail_templates.all()

    def clean_recipients(self):
        """
        Cleans the recipients list, removing duplicates and empty lines.
        """
        recipients_raw = self.cleaned_data.get("recipients", "")
        recipients_list = [
            email.strip()
            for email in recipients_raw.splitlines()
            if email.strip() and "@" in email
        ]
        if not recipients_list:
            raise forms.ValidationError(_("You need to provide at least one recipient."))
        return list(set(recipients_list))  # Remove duplicates

    def clean_bcc(self):
        """
        Cleans the BCC list, removing duplicates and empty lines.
        """
        bcc_raw = self.cleaned_data.get("bcc", "")
        if not bcc_raw:
            return []
        bcc_list = [
            email.strip()
            for email in bcc_raw.splitlines()
            if email.strip() and "@" in email
        ]
        return list(set(bcc_list))