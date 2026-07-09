from django.urls import path
from . import views

app_name = 'opportunities'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/match/', views.OpportunityMatchView.as_view(), name='match'),
]
