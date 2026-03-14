from django.db import models
from utils import BaseModel
from course.models import Course
from certification.models import Certification


class CourseCertificationMapping(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_certification_mappings')
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE, related_name='course_certification_mappings')
    primary_mapping = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']
        unique_together = [('course', 'certification')]

    def __str__(self):
        return f"Course({self.course_id}) → Certification({self.certification_id})"
