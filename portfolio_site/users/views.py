from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, View
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from .models import Subscription, UserProfile
from .forms import ProfileEditForm


class CustomLoginView(LoginView):
    template_name = 'users/login.html'


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_object(self):
        user_id = self.request.GET.get('user_id')
        if user_id:
            return get_object_or_404(User, id=user_id)
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tracked_products'] = self.request.user.userprofile.tracked_products.all()
        context['user_subscription'] = Subscription.objects.filter(user=self.get_object(), is_active=True).first()
        return context


class FollowAuthorView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        profile_to_follow = get_object_or_404(UserProfile, user__id=user_id)
        if profile_to_follow != request.user.userprofile: 
            request.user.userprofile.followed_authors.add(profile_to_follow)
        return HttpResponseRedirect(reverse('users:profile') + f'?user_id={user_id}')


class UnfollowAuthorView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        profile_to_unfollow = get_object_or_404(UserProfile, user__id=user_id)
        request.user.userprofile.followed_authors.remove(profile_to_unfollow)
        return HttpResponseRedirect(reverse('users:profile') + f'?user_id={user_id}')
    

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = ProfileEditForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user.userprofile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    