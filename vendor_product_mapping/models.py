from django.db import models
from utils import BaseModel
from vendor.models import Vendor
from product.models import Product


class VendorProductMapping(BaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor_product_mappings')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='vendor_product_mappings')
    primary_mapping = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']
        unique_together = [('vendor', 'product')]  # prevent duplicate pairs

    def __str__(self):
        return f"Vendor({self.vendor_id}) → Product({self.product_id})"
