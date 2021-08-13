from django.db import models
from django.utils import timezone
from django.contrib.auth.models import UserManager, AbstractUser
from django.utils.translation import gettext_lazy as _

from .validators import Validators

# Create your models here.
class MyUserManager(UserManager):
    """
    Customizing Manager of User for Change Auth Field to Phone Number for Default Username
    """

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        username = extra_fields["phone_number"]
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    """
    Customization User Model for Change Default User Name to Phone Number for Auth Pages
    """

    class Meta:
        verbose_name, verbose_name_plural = _("User"), _("Users")

    objects = MyUserManager()
    USERNAME_FIELD = 'phone_number'

    phone_number = models.CharField(max_length=11, unique=True, verbose_name=_("Phone Number"),
        validators=[Validators.check_phone_number], help_text=_("Please Enter Your Phone Number"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.phone_number = self.username


class BasicManager(models.Manager):
    """
    Basic Class Manager for Customize the Query Set and Filter by Deleted
    """

    # override get_queryset method to hide logical deleted in functions
    def get_queryset(self):
        return super().get_queryset().exclude(deleted=True)

    # override delete method to change deleted field to logical delete
    def delete(self):
        for obj in self:
            obj.delete()

    # create new method to set new all() function for show deleted item
    def archive(self):
        return super().get_queryset()


class BasicModel(models.Model):
    """
    Basic Class Model for Inheritance All Other Class Model from this
    """

    class Meta:
        abstract = True  # can't create instance object from this class
    
    objects = BasicManager()

    deleted = models.BooleanField(default=False, db_index=True)  # column indexing
    create_timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Create TimeStamp"))
    modify_timestamp = models.DateTimeField(auto_now=True)
    delete_timestamp = models.DateTimeField(default=None, null=True, blank=True)

    def delete(self):  # logical delete
        """
        Overrided Delete Method to Logical Delete Save the Record without Show
        """

        self.deleted = True
        self.delete_timestamp = timezone.now()
        self.save()


class TestModel(BasicModel):
    """
    This Class Just Written to Unit Test Basic Test Class Model
    """

    pass
