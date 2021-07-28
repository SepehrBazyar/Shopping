from django.core.exceptions import *
from django.utils.translation import gettext_lazy as _

from typing import Optional

class DiscountValidator:
    """
    Validator Callable Class for Check Percent Discount Between 0 and 100 Numbers
    """

    def __init__(self, unit: str):
        self.unit = unit
    
    def __call__(self, amount: int, roof: Optional[int]):
        if self.unit == 'P' and amount > 100:
            raise ValidationError(_("Percentage Rate Must be Between 0 & 100"))
        if self.unit == 'T' and roof:
            raise ValidationError(_("Ceiling Just in Percent Unit Available"))


class DatesValidator:
    """
    Validator Callable Class for Check End Date of Discount After the Start Date
    """

    def __init__(self, start_date):
        self.start_date = start_date
    
    def __call__(self, end_date):
        if end_date and end_date < self.start_date:
            raise ValidationError(_("End Date Should be After the Start Date"))
