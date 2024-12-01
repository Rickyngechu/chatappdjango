from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path('group/<int:group_id>/', views.group_chat, name='group_chat'),
    path('api/group_messages/<int:group_id>/', views.group_messages, name='group_messages'),
      # Route for group chat
]