from django.shortcuts import render, redirect
from django.utils import translation

# Create your views here.
def change_language(request):
    """
    Function to Change Language Automatic by Check Current LANGUAGE CODE
    """

    language = 'en' if translation.get_language() == 'fa' else 'fa'
    translation.activate(language)
    request.session[translation.LANGUAGE_SESSION_KEY] = language
    return redirect(request.GET.get('current', '/'))
