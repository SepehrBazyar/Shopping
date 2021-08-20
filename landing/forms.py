from django import forms

from .models import Message

class MessageForm(forms.ModelForm):
    """
    Model Form for Write New Message in Contact Page View
    """

    class Meta:
        model = Message
        exclude = ['deleted', 'delete_timestamp', 'was_read']


class SearchForm(forms.Form):
    """
    Form to Create Search Box in Home Page to Filter Product Item
    """

    search = forms.CharField()
