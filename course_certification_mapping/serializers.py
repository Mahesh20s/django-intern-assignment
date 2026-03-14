from rest_framework import serializers
from .models import CourseCertificationMapping


class CourseCertificationMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCertificationMapping
        fields = ['id', 'course', 'certification', 'primary_mapping', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        course = data.get('course', getattr(self.instance, 'course', None))
        certification = data.get('certification', getattr(self.instance, 'certification', None))
        primary_mapping = data.get('primary_mapping', getattr(self.instance, 'primary_mapping', False))

        # Duplicate pair check
        qs = CourseCertificationMapping.objects.filter(course=course, certification=certification)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "A mapping for this Course–Certification pair already exists."
            )

        # Only one primary_mapping per course
        if primary_mapping:
            primary_qs = CourseCertificationMapping.objects.filter(course=course, primary_mapping=True)
            if self.instance:
                primary_qs = primary_qs.exclude(pk=self.instance.pk)
            if primary_qs.exists():
                raise serializers.ValidationError(
                    "This Course already has a primary certification mapping."
                )

        return data
