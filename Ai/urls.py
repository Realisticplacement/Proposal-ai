from django.urls import path
from .views import AIExecutionListView, AIExecutionDetailView

urlpatterns = [
    path('ai-executions/', AIExecutionListView.as_view(), name='ai-execution-list'),
    path('ai-executions/<int:pk>/', AIExecutionDetailView.as_view(), name='ai-execution-detail'),
]