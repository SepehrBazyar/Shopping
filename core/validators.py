from django.core.exceptions import *
from django.utils.translation import gettext_lazy as _

import re as regex

class Validators:
    """
    Check Validation of the All the Input Values
    """

    PHONE_NUMBER_PATTERN = r"^(09)([0-9]{9})$"
    POSTAL_CODE_PATTERN = r"^([0-9]{10})$"

    @classmethod
    def check_phone_number(cls, phone_number: str):
        """
        Check Validation of Phone Number\n
        Example Valid Number: 09123456789
        """

        if not regex.search(cls.PHONE_NUMBER_PATTERN, phone_number):
            raise ValidationError(_("Phone Number Must Start with 09 & its Length is 11 Char."))

    @classmethod
    def check_postal_code(cls, postal_code: str):
        """
        Check Validation Zip Code 10 Digits
        """

        if not regex.search(cls.POSTAL_CODE_PATTERN, postal_code):
            raise ValidationError(_("Zip Code Must be 10 Digits."))
