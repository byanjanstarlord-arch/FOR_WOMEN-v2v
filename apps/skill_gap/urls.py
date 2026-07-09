from django.urls import path
from . import views

app_name = 'skill_gap'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/analyze/', views.SkillGapAnalyzeView.as_view(), name='analyze'),
]
