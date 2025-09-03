from django import forms

class InviteForm(forms.Form):
    template = forms.ChoiceField(
        label=_("Email Template"),
        choices=[],
    )
    to = forms.CharField(
        label=_("TO: (comma-separated email addresses, visible to recipients)"),
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )
    bcc = forms.CharField(
        label=_("BCC: (comma-separated email addresses, hidden from recipients)"),
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )

    def __init__(self, *args, event=None, **kwargs):
        super().__init__(*args, **kwargs)
        if event:
            choices = [
                (t.pk, t.subject.get(event.locale, t.subject.get("en", "Untitled")))
                for t in event.mail_templates.all().order_by("pk")
            ]
            self.fields["template"].choices = choices
