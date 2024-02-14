from django import forms
from .models import Policy, Claim
from django.utils import timezone

class PolicyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['value'] = timezone.now().strftime('%Y-%m-%d')
        self.fields['start_date'].widget.attrs['min'] = timezone.now().strftime('%Y-%m-%d')

    class Meta:
        model = Policy
        fields = ['start_date', 'end_date', 'type', 'lumpsum', 'premium']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ClaimForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['policy_number'] = forms.ModelChoiceField(queryset=Policy.objects.filter(user=user).values_list('policy_number', flat=True))

    class Meta:
        model = Claim
        fields = ['policy_number', 'amt', 'reason']