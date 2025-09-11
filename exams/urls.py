from django.urls import path, include
from .views import ExamDetailView, ExamListView, \
    ExamParticipationCreateView, ExamResultDetailView, exam_submitted, ExamPageView

urlpatterns = [
    path('', ExamListView.as_view(), name='exam-list'),
    path('exam/<pk>/detail/', ExamDetailView.as_view(), name='exam-detail'),
    path('exam/<pk>/start/', ExamParticipationCreateView.as_view(), name='exam-start'),
    path('exam/attempt/<pk>/', ExamPageView.as_view(), name='exam-page'),
    path('exam/<pk>/result/', ExamResultDetailView.as_view(), name='exam-result'),
    path('exam/submitted/', exam_submitted, name='exam-submitted'),
]
