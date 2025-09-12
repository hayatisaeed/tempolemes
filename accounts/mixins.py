from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileCompletionRequiredMixin(LoginRequiredMixin):
    """
    Mixin to ensure the logged-in user has completed their StudentProfile.
    If not, redirects to the dashboard.
    """

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        # If the user doesn't have a StudentProfile, or it's incomplete
        if (
            not hasattr(user, 'student_profile')
            or not user.student_profile.profile_completed
        ):
            return redirect(reverse('home'))

        return super().dispatch(request, *args, **kwargs)
