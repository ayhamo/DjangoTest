from django.urls import path
from django.views.generic import TemplateView

from .views import *

app_name = 'CourseApp'

urlpatterns = [
    path('', TemplateView.as_view(template_name="courseApp/index.html")),
    path('list', CourseInfo.as_view(), name="CourseInfo"),
    # path('<int:pk>', CourseInfo.as_view(), name="CourseInfo"),
    # path('list', CourseInfo.as_view(), name="CourseInfo"),
]
