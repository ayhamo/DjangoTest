from django.urls import path
from django.views.generic import TemplateView

from .views import *

app_name = 'CourseApp'

urlpatterns = [
    path('', TemplateView.as_view(template_name="courseApp/index.html")),
    path('list', CourseInfo.as_view(), name="CourseInfo"),
    path('filter', FilteredCourses.as_view(), name="FilteredCourses"),
    # path('filter', FilteredCourses.as_view(), name="course_list"),
    # path('filter/<int:pk>/', DetailedCourseInfo.as_view(), name='course_detail')
    # path('list', CourseInfo.as_view(), name="CourseInfo"),
]
