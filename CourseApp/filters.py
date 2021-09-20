from django_filters import rest_framework as filters
from .models import *

# class CourseFilter(filters.FilterSet):
#     class Meta:
#         model = Course
#         fields = {'course_type', 'price'}

CHOICES = (('online', 1), ('offline', 0),)


def strtoint(val):
    val = val.lower()
    if val in ('online', '1'):
        return 1
    elif val in ('offline', '0'):
        return 0
    else:
        raise ValueError("invalid truth value %r" % (val,))


class CourseFilter(filters.FilterSet):
    course_type = filters.TypedChoiceFilter(choices=CHOICES, coerce=strtoint)
    price = filters.RangeFilter()

    class Meta:
        model = Course
        fields = {'course_type', 'price'}
