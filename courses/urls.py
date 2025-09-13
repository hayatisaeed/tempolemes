from django.urls import path, include
from .views import CourseListView, CourseDetailView, CourseEnrollmentCreateView, EnrolledCourseListView, EnrolledCourseDetailView

urlpatterns = [
    path('', CourseListView.as_view(), name='course-list'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('course/<int:course_pk>/enroll/', CourseEnrollmentCreateView.as_view(), name='course-enroll'),
    path('my/', EnrolledCourseListView.as_view(), name='enrolled-course-list'),
    path('my/<int:pk>/', EnrolledCourseDetailView.as_view(), name='enrolled-course-detail'),
]