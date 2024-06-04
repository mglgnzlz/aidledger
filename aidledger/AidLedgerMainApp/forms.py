from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, QRCode

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('accountName', 'userType', 'username')


class qrForm(forms.ModelForm):
    class Meta:
        model = QRCode
        fields = ['qr_image']