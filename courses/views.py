from django.shortcuts import render
from accounts.mixins import ProfileCompletionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Course, CourseEnrollment
from django.urls import reverse_lazy
from django.shortcuts import redirect


class CourseListView(ProfileCompletionRequiredMixin, ListView):
    template_name = "courses/course_list.html"
    context_object_name = "courses"
    paginate_by = 10

    def get_queryset(self):
        return Course.objects.all()


class CourseDetailView(ProfileCompletionRequiredMixin, DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"


class CourseEnrollmentCreateView(ProfileCompletionRequiredMixin, CreateView):
    model = CourseEnrollment
    template_name = "courses/course_enrollment_form.html"
    fields = []

    def dispatch(self, request, *args, **kwargs):
        # TODO: implement logic for enrolling in a course
        # right now, this will enroll the user in the course with no restrictions
        course_pk = self.kwargs.get('course_pk')
        course = Course.objects.get(pk=course_pk)
        CourseEnrollment.objects.get_or_create(course=course, student=request.user)
        return redirect('enrolled-course-detail', pk=course.pk)
        # return super().dispatch(request, *args, **kwargs)


class EnrolledCourseListView(ProfileCompletionRequiredMixin, ListView):
    template_name = "courses/course_enrollment_list.html"
    context_object_name = "enrollments"
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.course_enrollments.select_related('course').all()


class EnrolledCourseDetailView(ProfileCompletionRequiredMixin, DetailView):
    model = Course
    template_name = "courses/course_enrollment_detail.html"
    context_object_name = "course"

    def get_queryset(self):
        # Only courses the user is enrolled in
        return Course.objects.filter(enrollments__student=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the enrollment object for the logged-in user
        context['enrollment'] = self.object.enrollments.get(student=self.request.user)
        return context
