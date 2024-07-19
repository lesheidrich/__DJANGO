from django.urls import path
from basic_app import views

app_name = 'basic_app'  # actual app name for template tagging

urlpatterns = [
    path('relative/', views.relative, name='relative'),
    path('other/', views.other, name='other'),
]
