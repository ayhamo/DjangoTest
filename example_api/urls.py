from django.urls import path

from .views import PostList, PostDetail

app_name = 'example_api'

urlpatterns = [
    path('<int:pk>', PostDetail.as_view(), name="detailcreate"),
    path('api/', PostList.as_view(), name="listcreate"),
]
