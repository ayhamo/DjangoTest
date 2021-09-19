from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializer import *


class CourseInfo(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


# @api_view(['GET'])
# def course_list(request):
#     courses = []
#     for course in Course.objects.all():
#         courses.append(CourseSerializer(course).data)  # data returns map
#
#     return Response(courses)


class OnlineCourseInfo(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = OnlineCourseSerializer
