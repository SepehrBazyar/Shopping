from .utils import readable
from order.models import Order

def incoming(request):
    """
    Function for Pass this Context to All Templates and Access from Any Where
    """

    return {'income': readable(Order.total_income())}
