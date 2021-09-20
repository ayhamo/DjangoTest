from django_filters import rest_framework as filters
from .models import *


class CourseFilter(filters.FilterSet):
    class Meta:
        model = Course
        fields = {'course_type', 'price'}


# class CourseFilter(django_filters.FilterSet):
#     course_type = django_filters.NumberFilter()
#     price = django_filters.NumberFilter()
#
#     class Meta:
#         model = Course
