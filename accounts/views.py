from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import StudentProfile
from django.shortcuts import redirect
from django.urls import reverse


class UserRegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/register.html'  # your template path
    success_url = reverse_lazy('login')  # where to redirect after successful registration

    def form_valid(self, form):
        # Save the new user
        response = super().form_valid(form)
        # You can add extra logic here if needed (like sending a welcome email)
        return response



class UserLoginView(LoginView):
    template_name = 'accounts/login.html'          # your login template
    redirect_authenticated_user = True            # already logged-in users get redirected
    # by default it uses AuthenticationForm (username + password)
    # you can override success_url if needed:

    def get_success_url(self):
        return reverse_lazy('home')  # or wherever you want to redirect after login


class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('login')  # where to send the user after logout
    http_method_names = ['get', 'post']  # allow GET and POST

    def get(self, request, *args, **kwargs):
        """
        Allow logout via GET request.
        """
        return self.post(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = StudentProfile.objects.filter(user=self.request.user).first()
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'student_profile') or not request.user.student_profile.profile_completed:
            return redirect(reverse('profile-update'))
        return super().dispatch(request, *args, **kwargs)
    

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = StudentProfile
    template_name = 'accounts/profile_update.html'
    fields = [
        'first_name',
        'last_name',
        'national_code',
        'phone_number',
        'parents_phone_number',
        'bio',
        'birthdate_day',
        'birthdate_month',
        'birthdate_year',
    ]
    success_url = reverse_lazy('home')  # or wherever you want

    def get_object(self, queryset=None):
        """
        Always return the profile of the logged-in user.
        Create it if it doesn't exist.
        """
        obj, created = StudentProfile.objects.get_or_create(user=self.request.user)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        return context
    