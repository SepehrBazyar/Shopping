from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Message

class MessageForm(forms.ModelForm):
    """
    Model Form for Write New Message in Contact Page View
    """

    class Meta:
        model = Message
        exclude = ['deleted', 'delete_timestamp', 'was_read']
