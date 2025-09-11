from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Exam, ExamParticipation, ExamResult
from courses.models import Course
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse


class ExamListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = 'exams/exam_list.html'
    context_object_name = 'exams'

    def get_queryset(self):
        return Exam.objects.all().filter(related_course__in=self.request.user.course_enrollments.values_list('course', flat=True))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.filter(enrollments__student=self.request.user)
        return context


class ExamDetailView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = 'exams/exam_detail.html'
    context_object_name = 'exam'

    def get_queryset(self):
        """
        Limit exams to only those the user is allowed to access.
        """
        user = self.request.user
        allowed_courses = user.course_enrollments.values_list('course', flat=True)
        return Exam.objects.filter(related_course__in=allowed_courses)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam = self.get_object()
        participation = ExamParticipation.objects.filter(exam=exam, student=self.request.user).first()
        context['can_start'] = not participation.completed if participation else True
        context['can_view_result'] = ExamResult.objects.filter(participation__exam=exam, participation__student=self.request.user).exists()
        return context




class ExamParticipationCreateView(LoginRequiredMixin, View):
    """
    This view just ensures an ExamParticipation exists for the user,
    then redirects to the exam page.
    """
    def get(self, request, *args, **kwargs):
        exam = get_object_or_404(Exam, pk=kwargs['pk'])
        start_date = timezone.now()

        # 1. Check enrollment
        if not request.user.course_enrollments.filter(course=exam.related_course).exists():
            return render(request, 'exams/not_allowed.html', status=403)

        # 2. Get or create participation
        participation, created = ExamParticipation.objects.get_or_create(
            exam=exam,
            student=request.user,
        )

        if created:  # add start_date if newly created
            participation.start_date = start_date
            participation.save()

        # 3. Redirect to exam page
        return redirect('exam-page', pk=participation.pk)


class ExamPageView(LoginRequiredMixin, UpdateView):
    model = ExamParticipation
    template_name = 'exams/exam_page.html'
    fields = ['answer_file']  # only show answer_file
    success_url = reverse_lazy('exam-submitted')

    def dispatch(self, request, *args, **kwargs):
        """
        Before showing the page, ensure the user has a participation.
        If not, redirect back to exam-detail.
        """
        participation_pk = kwargs.get('pk')
        participation = get_object_or_404(ExamParticipation, pk=participation_pk)
        exam_pk = participation.exam.pk

        self.participation = participation  # store for later use

        if not self.participation:
            # Redirect if participation doesn't exist yet
            return redirect('exam-detail', pk=exam_pk)
        
        # Check ownership
        if self.participation.student != request.user:
            return render(request, 'exams/not_allowed.html', status=403)
        if self.participation.completed:
            return render(request, 'exams/not_allowed.html', status=403)
        
        # Check time limit
        end_time = self.participation.start_date + timezone.timedelta(minutes=self.participation.exam.duration_minutes)
        if timezone.now() > end_time:
            return render(request, 'exams/time_up.html', status=403)

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Restrict to the logged-in user's active participations.
        """
        return ExamParticipation.objects.filter(student=self.request.user, completed=False)

    from django.http import JsonResponse

    def form_valid(self, form):
        # Only mark completed after saving the file
        # This ensures upload actually succeeded
        saved_instance = form.save(commit=False)  # don't save yet
        saved_instance.completed = True
        saved_instance.completion_date = timezone.now()
        saved_instance.save()  # now save to DB

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # return 200 without redirect
            return JsonResponse({'success': True})
        
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        participation = self.participation
        exam = participation.exam
        context['participation'] = participation
        context['exam'] = exam
        context['end_time'] = participation.start_date + timezone.timedelta(minutes=exam.duration_minutes)
        return context
    

class ExamResultDetailView(LoginRequiredMixin, DetailView):
    model = ExamResult
    template_name = 'exams/exam_result.html'
    context_object_name = 'result'

    def get_object(self, queryset=None):
        """
        Return the ExamResult object only if the user is allowed to access it.
        """
        user = self.request.user
        exam_result = get_object_or_404(
            ExamResult,
            pk=self.kwargs.get('pk'),
            participation__student=user,
            participation__exam__related_course__in=user.course_enrollments.values_list('course', flat=True)
        )
        return exam_result
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result = self.get_object()
        context['student_name'] = result.participation.student
        context['exam_name'] = result.participation.exam.title
        context['start_date'] = result.participation.start_date
        return context


def exam_submitted(request):
    return render(request, 'exams/exam_submitted.html')
