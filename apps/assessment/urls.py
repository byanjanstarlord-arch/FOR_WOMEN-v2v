from django.urls import path
from . import views

app_name = 'assessment'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/analyze/', views.AssessmentAnalyzeView.as_view(), name='analyze'),
]
