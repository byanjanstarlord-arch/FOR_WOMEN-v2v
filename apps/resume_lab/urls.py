from django.urls import path
from . import views

app_name = 'resume_lab'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/analyze/', views.ResumeAnalyzeView.as_view(), name='analyze'),
]
