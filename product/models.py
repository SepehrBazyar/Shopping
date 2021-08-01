from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import *
from django.utils.translation import get_language, gettext_lazy as _

from pymongo import MongoClient
from bson.objectid import ObjectId  # for convert string id to searchable id mongodb

from typing import List, Dict

from core.models import BasicModel
from .validators import *
from .utils import *

# Create your models here.
class DynamicTranslation(BasicModel):
    """
    Abstract Model for Save Bilingual Dynamic String and Manage by LANGUAGE_CODE
    """

    class Meta:
        abstract = True  # can't create instance object from this class

    title_en = models.CharField(max_length=100, unique=True, verbose_name=_("English Title"),
                                help_text=_("Please Enter the Title of the Name in English"))
    title_fa = models.CharField(max_length=100, unique=True, verbose_name=_("Persian Title"),
                                help_text=_("Please Enter the Title of the Name in Persian"))
    slug = models.SlugField(verbose_name=_("Slug"), help_text=_("Please Type Your Slug"))
    
    @property
    def title(self) -> str:
        """
        Property Method to Get the Translated Dynamic String by LANGUAGE_CODE
        """

        return self.title_fa if get_language() == 'fa' else self.title_en
    
    def __str__(self) -> str:
        return self.title


class Category(DynamicTranslation):
    """
    Model of Category for Product Items with Self Relations\n
    Because For Example Laptops is a SubCategory of Digitals.
    """

    class Meta:
        verbose_name, verbose_name_plural = _("Category"), _("Categories")

    root = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=_("Main Category"), help_text=_("Please Select the Main Category"))
    properties = models.CharField(max_length=24, null=True, default=None)  # mongodb object id

    def add_property(self, en_name: str, fa_name: str) -> List[str]:
        """
        Create New Property for this Category with Name in Two Languages
        """

        with MongoClient('mongodb://localhost:27017/') as client:
            categories = client.shopping.categories
            props = categories.find_one({
                "_id": ObjectId(self.properties)
                },
                {
                    "_id": 0, "en": 1, "fa": 1
                }
            )

            props["en"].append(en_name)
            props["fa"].append(fa_name)

            categories.update_one({
                "_id": ObjectId(self.properties)
                },
                {
                    '$set': {
                        "en": props["en"],
                        "fa": props["fa"]
                    }
                }
            )
        
        return self.property_list()
    
    def delete_property(self, name: str, lang: str = get_language()) -> List[str]:
        """
        Delete a Property by Get the Name and Find it in Language Code Lists
        """

        with MongoClient('mongodb://localhost:27017/') as client:
            categories = client.shopping.categories
            props = categories.find_one({
                "_id": ObjectId(self.properties)
                },
                {
                    "_id": 0, "en": 1, "fa": 1
                }
            )
            
            try:
                index = props[lang].index(name)
            except ValueError:
                pass
            else:
                props["en"].pop(index)
                props["fa"].pop(index)

                categories.update_one({
                    "_id": ObjectId(self.properties)
                    },
                    {
                        '$set': {
                            "en": props["en"],
                            "fa": props["fa"]
                        }
                    }
                )

        return self.property_list(lang)

    def property_list(self, lang: str = get_language()) -> List[str]:
        """
        Show a List of All the Property for this Category by Language
        """

        with MongoClient('mongodb://localhost:27017/') as client:
            categories = client.shopping.categories
            props = categories.find_one({
                "_id": ObjectId(self.properties)
                },
                {
                    "_id": 0, "en": 1, "fa": 1
                }
            )

        return props[lang]

    def save(self, *args, **kwargs):
        if self.properties is None:
            with MongoClient('mongodb://localhost:27017/') as client:
                categories = client.shopping.categories
                result = categories.insert_one({"en": [], "fa": []})
                self.properties = result.inserted_id
        return super(self.__class__, self).save(*args, **kwargs)


class Brand(DynamicTranslation):
    """
    Model of Brand for Save Company Informations and Products
    """

    class Meta:
        verbose_name, verbose_name_plural = _("Brand"), _("Brands")

    logo = models.FileField(upload_to="product/brands/", verbose_name=_("Logo"),
                            default="Unknown.jpg", blank=True,
                            help_text=_("Please Upload the Logo Icon of Brand"))
    link = models.URLField(max_length=200, default=None, null=True, blank=True,
                        verbose_name=_("Website Address"), validators=[URLValidator],
                        help_text=_("Please Enter Your Website Address"))


class Discount(DynamicTranslation):
    """
    Model of Discount for Apply on Product Items Price
    """

    class Meta:
        verbose_name, verbose_name_plural = _("Discount"), _("Discounts")
    
    UNITS = {
        'P': _("Percent"),
        'T': _("Toman"),
    }

    unit = models.CharField(max_length=1, choices=[(key, value) for key, value in UNITS.items()],
                            verbose_name=_("Unit"), help_text=_("Please Select the Discount Unit"))
    amount = models.PositiveBigIntegerField(default=0, verbose_name=_("Discount Amount"),
                                            help_text=_("Please Enter Discount Amount"))
    roof = models.PositiveBigIntegerField(default=None, null=True, blank=True,
        verbose_name=_("Discount Ceiling"), help_text=_("Please Enter Discount Ceiling(Optional)"))
    start_date = models.DateTimeField(default=timezone.now, null=True, blank=True,
        verbose_name=_("Start Date"), help_text=_("Please Select the Start Date of the Discount"))
    end_date = models.DateTimeField(default=None, null=True, blank=True,
        verbose_name=_("End Date"), help_text=_("Please Select the End Date of the Discount"))

    def calculate_price(self, price: int) -> int:
        """
        Calculate the Price Paid After Applying the Discount
        """

        decrease, present = 0, timezone.now()
        if self.start_date <= present:
            if self.end_date is None or present <= self.end_date:
                if self.unit == 'T':
                    decrease = self.amount
                else:
                    decrease = price * self.amount // 100
                    if self.roof is not None:
                        decrease = min(decrease, self.roof)

        return max(price - decrease, 0)

    def clean(self):
        """
        Validating Field Data Based on Another Field's Value
        """

        DiscountValidator(self.unit)(self.amount, self.roof)
        DatesValidator(self.start_date)(self.end_date)

    def __str__(self) -> str:
        mx_trans = _("Maximum")
        desc = f"({mx_trans}: {self.roof} {self.UNITS['T']})" if self.roof is not None else ""
        return f"{self.amount} {self.UNITS[self.unit]}{desc}"


class Product(DynamicTranslation):
    """
    Model of Product Items for Save Detail Information for Show in Home Page
    """

    class Meta:
        verbose_name, verbose_name_plural = _("Product"), _("Products")
    
    image = models.FileField(upload_to="product/products/", verbose_name=_("Picture"),
                            default="Unknown.jpg", blank=True,
                            help_text=_("Please Upload a Picture of the Product Item"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products",
        verbose_name=_("Category"), help_text=_("Please Select the Category of the Product Item"))
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products",
        verbose_name=_("Brand"), help_text=_("Please Select the Brand of the Product Item"))
    price = models.PositiveBigIntegerField(verbose_name=_("Price"),
        help_text=_("Please Enter the Price of Product Item without Apply Discount"))
    inventory = models.PositiveBigIntegerField(verbose_name=_("Number of Inventory"),
        help_text=_("Please Enter the Number of this Product Item into the Stock"))
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name="products",
                                verbose_name=_("Discount"), default=None, null=True, blank=True,
                                help_text=_("Please Select the Type of Discount if Available"))
    properties = models.CharField(max_length=24, null=True, default=None)  # mongodb object id

    @property
    def final_price(self) -> int:
        """
        Property Method to Calculate Final Price by Apply Discount Changes
        """

        result = self.price
        if self.discount is not None:
            result = self.discount.calculate_price(result)
        return result
    final_price.fget.short_description = _("Final Price")  # like verbose name for panel admin

    @property
    def readable_price(self) -> str:
        """
        Spilted Digites of Price Product with / by Step 3
        """

        return readable(self.price)
    
    @property
    def readable_final_price(self) -> str:
        """
        Spilted Digites of Final Price Product with / by Step 3
        """

        return readable(self.final_price)
    
    @property
    def check_discount(self) -> bool:
        """
        Check Discount is Apply or Not For Example Expire End Date
        """

        return self.price != self.final_price
    
    @property
    def property_list(self) -> Dict[str, str]:
        """
        Property Method to Return Dict of Properties for Templates
        """

        return self.read_property()

    def read_property(self, property_name: str = None, lang: str = get_language()):
        """
        Read All or One Property of this Product Item by Category List in MongoDB
        """

        with MongoClient('mongodb://localhost:27017/') as client:
            products = client.shopping.products
            props = products.find_one({
                "_id": ObjectId(self.properties)
                },
                {
                    "_id": 0, "en": 1, "fa": 1
                }
            )
        
        return props[lang].get(property_name, props[lang])

    def write_property(self, property_name: str, new_value, lang: str = get_language()):
        """
        Write a Value for Property Name in MongoDB Document by Language Code Default
        """

        with MongoClient('mongodb://localhost:27017/') as client:
            products = client.shopping.products
            props = products.find_one({
                "_id": ObjectId(self.properties)
                },
                {
                    "_id": 0, "en": 1, "fa": 1
                }
            )

            prop = props[lang]
            try:
                prop[property_name]
            except KeyError:
                pass
            else:
                prop[property_name] = new_value
                products.update_one({
                    "_id": ObjectId(self.properties)
                    },
                    {
                        '$set': {
                            lang: prop
                        }
                    }
                )

        return self.read_property(lang=lang)

    def save(self, *args, **kwargs):
        if self.properties is None:
            with MongoClient('mongodb://localhost:27017/') as client:
                products = client.shopping.products
                en, fa = {}, {}
                for item in self.category.property_list("en"):
                    en[item] = ""
                for item in self.category.property_list("fa"):
                    fa[item] = ""
                result = products.insert_one({"en": en, "fa": fa})
                self.properties = result.inserted_id
        return super(self.__class__, self).save(*args, **kwargs)

    def __str__(self) -> str:
        toman_trans = _("Toman")
        return f"{self.title} - {self.readable_final_price} {toman_trans}"
