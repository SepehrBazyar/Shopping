from ._basestaff import BasicCommand

class Command(BasicCommand):
    """
    Command Class to Change User to is not Staff
    """

    help = "Choose User for Leave from Staffs"

    def handle(self, *args, **options):
        user = super().handle(*args, **options)
        user.is_staff = False
        user.save()
        self.stdout.write(self.style.WARNING(f"User {user.username} is not Staff."))
