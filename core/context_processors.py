from typing import Dict

from .utils import readable
from customer.models import Customer
from order.models import Order

def incoming(request) -> Dict[str, str]:
    """
    Function for Pass Total Incoming Context to All Templates
    """

    return {'income': readable(Order.total_income())}
