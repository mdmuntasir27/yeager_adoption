from django import forms
from .models import AdoptionRequest


class AdoptionRequestForm(forms.ModelForm):
    previous_pet_experience = forms.ChoiceField(
        choices=[('True', 'Yes'), ('False', 'No')],
        widget=forms.RadioSelect,
        label='Have you owned a pet before?'
    )

    class Meta:
        model = AdoptionRequest
        fields = ['phone', 'address', 'reason', 'previous_pet_experience', 'message']
        labels = {
            'phone': 'Phone Number',
            'address': 'Address',
            'reason': 'Why do you want this pet?',
            'message': 'Additional Message (optional)',
        }
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'e.g. 01XXXXXXXXX', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Your full address', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us why you want to adopt this pet...', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any additional message...', 'class': 'form-control'}),
        }

    def clean_previous_pet_experience(self):
        value = self.cleaned_data['previous_pet_experience']
        return value == 'True'
