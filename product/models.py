from django.db import models
from django.utils.translation import get_language, gettext_lazy as _

from core.models import BasicModel

# Create your models here.
class DynamicTranslation(BasicModel):
    """
    Abstract Model for Save Bilingual Dynamic String and Manage by LANGUAGE_CODE
    """

    class Meta:
        abstract = True

    title_en = models.CharField(max_length=100, unique=True, verbose_name=_("English Title"),
                                help_text=_("Please Enter the Title of the Name in English"))
    title_fa = models.CharField(max_length=100, unique=True, verbose_name=_("Persian Title"),
                                help_text=_("Please Enter the Title of the Name in Persian"))
    
    @property
    def title(self) -> str:
        """
        Property Method to Get the Translated Dynamic String by LANGUAGE_CODE
        """

        return self.title_fa if get_language() == 'fa' else self.title_en


class Category(DynamicTranslation):
    """
    Model of Category for Product Items with Self Relations\n
    Because For Example Laptops is a SubCategory of Digitals.
    """

    class Meta:
        verbose_name, verbose_name_plural = _("Category"), _("Categories")
    
    root = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=_("Main Category"), help_text=_("Please Select the Main Category"))
    
    def __str__(self) -> str:
        result = ""
        if self.root:
            result += self.root.__str__() + ' > '
        return result + self.title
