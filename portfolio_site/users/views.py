from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, View
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.conf import settings
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from .models import Subscription, UserProfile
from .forms import ProfileEditForm, SubscriptionForm
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


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
        context['user_subscription'] = Subscription.objects.filter(user=self.request.user, is_active=True).first()
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


class SubscriptionCreateView(LoginRequiredMixin, FormView):
    form_class = SubscriptionForm
    template_name = 'users/subscribe.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        plan = form.cleaned_data['plan']
        price_id = settings.STRIPE_PRICE_ID_MONTHLY if plan == 'monthly' else settings.STRIPE_PRICE_ID_YEARLY
        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email=self.request.user.email,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f"{settings.SITE_DOMAIN}{reverse('users:subscription_success')}?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.SITE_DOMAIN}{reverse('users:profile')}",
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)


class SubscriptionSuccessView(LoginRequiredMixin, View):
    def get(self, request):
        session_id = request.GET.get('session_id')
        if not session_id:
            return redirect('users:profile')

        try:
            checkout_session = stripe.checkout.Session.retrieve(session_id)
            subscription = stripe.Subscription.retrieve(checkout_session.subscription)
            plan = 'monthly' if subscription.plan.id == settings.STRIPE_PRICE_ID_MONTHLY else 'yearly'
            
            sub, created = Subscription.objects.get_or_create(
                user=self.request.user,
                defaults={
                    'plan': plan,
                    'start_date': timezone.now(),
                    'end_date': timezone.now() + timezone.timedelta(days=30 if plan == 'monthly' else 365),
                    'is_active': True,
                    'stripe_subscription_id': subscription.id
                }
            )
            if not created:
                sub.plan = plan
                sub.end_date = timezone.now() + timezone.timedelta(days=30 if plan == 'monthly' else 365)
                sub.is_active = True
                sub.stripe_subscription_id = subscription.id
                sub.save()

            return render(request, 'users/subscription_success.html', {'subscription': sub})
        except Exception as e:
            return redirect('users:profile')
        
