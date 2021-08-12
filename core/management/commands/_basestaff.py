from django.core.management.base import BaseCommand, CommandError

from argparse import ArgumentParser

from core.models import User

class BasicCommand(BaseCommand):
    """
    Basic Class for Inheritanced to Change is_staff of Users
    """

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('username', metavar="Username", help="Please Enter Username")
    
    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f"User {username} Does Not Exist!")
        else:
            return user
