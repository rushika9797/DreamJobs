from django import forms
from .models import Job, Application
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):

    ROLE_CHOICES = (
        ("employer", "Employer"),
        ("seeker", "Job Seeker"),
    )

    email = forms.EmailField()

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect   # ⭐ radio buttons
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "role"]


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title','company','location','description']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume']   # 🔥 ONLY resume

