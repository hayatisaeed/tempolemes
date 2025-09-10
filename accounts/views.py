from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView, TemplateView


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


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # where to send the user after logout


class DashboardView(TemplateView):
    template_name = 'accounts/dashboard.html'  # your dashboard template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context