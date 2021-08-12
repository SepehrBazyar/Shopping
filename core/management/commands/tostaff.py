from ._basestaff import BasicCommand

class Command(BasicCommand):
    """
    Command Class to Change User to is Staff
    """

    help = "Choose User for Convert to Staff"

    def handle(self, *args, **options):
        user = super().handle(*args, **options)
        user.is_staff = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f"User {user.username} is Staff."))
