from rest_framework import generics

from .models import *
from .serializer import *
from .filters import *


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

class FilteredCourses(generics.ListCreateAPIView):
    model = Course
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CourseFilter

# class FilteredCourses(ListView):
#     model = Course
#     template_name = 'courseApp/course_list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['filter'] = CourseFilter(self.request.GET, queryset=self.get_queryset())
#         return context


# class DetailedCourseInfo(generics.):
#     model = Course
#     template_name = 'courseApp/course_detail.html'
