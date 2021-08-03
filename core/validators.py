from django.core.exceptions import *
from django.utils.translation import gettext_lazy as _

import re as regex

class Validators:
    """
    Check Validation of the All the Input Values
    """

    PHONE_NUMBER_PATTERN = r"^(09)([0-9]{9})$"

    @classmethod
    def check_phone_number(cls, phone_number: str):
        """
        Check Validation of Phone Number\n
        Example Valid Number: 09123456789
        """

        if not regex.search(cls.PHONE_NUMBER_PATTERN, phone_number):
            raise ValidationError(_("Phone Number Must be Start with 09 & Length is 11 Char."))
