from django import forms
from .models import UserProfile, Subscription
from django.contrib.auth.models import User


class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField(label='Email', required=True)

    class Meta:
        model = UserProfile
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=commit)
        user = profile.user
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return profile


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['plan']
        widgets = {
            'plan': forms.RadioSelect
        }
