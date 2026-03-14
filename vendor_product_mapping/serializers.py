from rest_framework import serializers
from .models import VendorProductMapping


class VendorProductMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProductMapping
        fields = ['id', 'vendor', 'product', 'primary_mapping', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        vendor = data.get('vendor', getattr(self.instance, 'vendor', None))
        product = data.get('product', getattr(self.instance, 'product', None))
        primary_mapping = data.get('primary_mapping', getattr(self.instance, 'primary_mapping', False))

        # Duplicate pair check
        qs = VendorProductMapping.objects.filter(vendor=vendor, product=product)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "A mapping for this Vendor–Product pair already exists."
            )

        # Only one primary_mapping per vendor
        if primary_mapping:
            primary_qs = VendorProductMapping.objects.filter(vendor=vendor, primary_mapping=True)
            if self.instance:
                primary_qs = primary_qs.exclude(pk=self.instance.pk)
            if primary_qs.exists():
                raise serializers.ValidationError(
                    "This Vendor already has a primary product mapping."
                )

        return data
