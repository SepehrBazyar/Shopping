from django.core.exceptions import *
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

def birthday_validator(birth_day):
    """
    Validator Function for Check Validated Birth Day Time Before Now
    """

    if not birth_day < now():
        raise ValidationError(_("Your Birth Day Can't be After Now Date Time"))
