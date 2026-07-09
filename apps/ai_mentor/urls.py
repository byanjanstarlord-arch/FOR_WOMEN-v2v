from django.urls import path
from . import views

app_name = 'ai_mentor'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/chat/', views.MentorChatView.as_view(), name='chat'),
]
