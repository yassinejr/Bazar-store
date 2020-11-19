from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Brand(models.Model):
    brand_name = models.CharField(max_length=40, null=True, verbose_name=_('Brand'))
    brand_description = models.TextField(max_length=500, null=True, default='', verbose_name=_('Description'))

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return str(self.brand_name)


class Variant(models.Model):
    variant_name = models.CharField(max_length=40, null=True, verbose_name=_('Variant'))
    variant_description = models.TextField(max_length=500, null=True, default='', verbose_name=_('Description'))

    class Meta:
        verbose_name = _("Variant")
        verbose_name_plural = _("Variants")

    def __str__(self):
        return str(self.variant_name)
