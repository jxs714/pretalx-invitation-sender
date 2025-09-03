from django import forms
from django.utils.translation import gettext_lazy as _

from pretalx.mail.models import MailTemplate


class InvitationForm(forms.Form):
    # Field for TO addresses
    to_recipients = forms.CharField(
        label=_("To"),
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text=_("Enter email addresses, one per line."),
        required=True,
    )

    # Field for BCC addresses
    bcc_recipients = forms.CharField(
        label=_("BCC"),
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text=_("Enter email addresses, one per line."),
        required=False,
    )

    # Dropdown to select an email template
    template = forms.ModelChoiceField(
        label=_("Email Template"),
        queryset=MailTemplate.objects.none(),  # Queryset is set dynamically in the view
        required=True,
    )

    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")
        super().__init__(*args, **kwargs)
        # Dynamically populate the template choices for the specific event
        self.fields["template"].queryset = MailTemplate.objects.filter(event=event)
