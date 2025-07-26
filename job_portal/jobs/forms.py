from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Job, Application

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role=self.cleaned_data['role']
            )
        return user

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company_name', 'location', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
        }

class JobSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by job title, company, or location...',
            'class': 'form-control'
        })
    )

