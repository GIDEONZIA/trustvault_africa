from django.shortcuts import render

# Create your views here.
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import User

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'phone_number']
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('accounts:profile_update')

    def get_object(self):
        return self.request.user
