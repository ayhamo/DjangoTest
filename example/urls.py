from django.urls import path
from django.views.generic import TemplateView

app_name = 'example'

urlpatterns = [
    path('', TemplateView.as_view(template_name="example/index.html"))
]
