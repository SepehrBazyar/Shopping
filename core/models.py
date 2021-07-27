from django.db import models
from django.utils import timezone

# Create your models here.
class BasicManager(models.Manager):
    """
    Basic Class Manager for Customize the Query Set and Filter by Deleted
    """

    # override get_queryset method to hide logical deleted in functions
    def get_queryset(self):
        return super().get_queryset().exclude(deleted=True)

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
    create_timestamp = models.DateTimeField(auto_now_add=True)
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
