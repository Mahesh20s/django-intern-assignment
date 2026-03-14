from django.db import models
from utils import BaseModel
from product.models import Product
from course.models import Course


class ProductCourseMapping(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_course_mappings')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='product_course_mappings')
    primary_mapping = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']
        unique_together = [('product', 'course')]

    def __str__(self):
        return f"Product({self.product_id}) → Course({self.course_id})"
