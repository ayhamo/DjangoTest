from django.urls import path
from django.views.generic import TemplateView

# from .views import PostList, PostDetail

app_name = 'CourseApp'

urlpatterns = [
    path('', TemplateView.as_view(template_name="courseApp/index.html")),
    # path('<int:pk>', PostDetail.as_view(), name="detailcreate"),
    # path('list/', PostList.as_view(), name="listcreate"),
]
