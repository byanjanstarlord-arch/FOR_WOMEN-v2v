from django.urls import path
from . import views

app_name = 'roadmap'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/generate/', views.RoadmapGenerateView.as_view(), name='generate'),
]
