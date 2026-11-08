from django import forms
from .models import AdoptionPost, AdoptionInquiry


class AdoptionPostForm(forms.ModelForm):
    class Meta:
        model = AdoptionPost
        fields = ['pet_name', 'animal_type', 'breed', 'age', 'gender', 'location', 'description', 'image']
        labels = {
            'pet_name': 'Pet Name',
            'animal_type': 'Animal Type',
            'breed': 'Breed (optional)',
            'age': 'Age in Years (optional)',
            'gender': 'Gender',
            'location': 'Location',
            'description': 'About the Pet',
            'image': 'Photo (optional)',
        }
        widgets = {
            'pet_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Max',
            }),
            'animal_type': forms.Select(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Golden Retriever',
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Age in years',
                'min': 0,
            }),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Dhaka, Mirpur',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tell others about this pet — temperament, health, reason for giving for adoption...',
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class AdoptionInquiryForm(forms.ModelForm):
    class Meta:
        model = AdoptionInquiry
        fields = ['message', 'contact_phone', 'contact_address']
        labels = {
            'message': 'Why do you want to adopt this pet?',
            'contact_phone': 'Your Phone Number',
            'contact_address': 'Your Address',
        }
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share a little about yourself and why this pet would be a good fit...',
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 01XXXXXXXXX',
            }),
            'contact_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Your full address',
            }),
        }


class InquiryStatusForm(forms.ModelForm):
    class Meta:
        model = AdoptionInquiry
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

