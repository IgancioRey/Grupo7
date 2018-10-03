
from django import forms
from . models import *
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User



class formRegistracion(forms.Form):
	nombreUsuario = forms.CharField(max_length=25, label='Usuario', widget=forms.TextInput(attrs={'class' : 'validate'}))
	email = forms.EmailField(label='Email',max_length=100, widget=forms.EmailInput(attrs={'class' : 'validate'}))
	password = forms.CharField(max_length=25, label='Contraseña', widget=forms.PasswordInput(attrs={'class' : 'validate'}))
	confpassword = forms.password=forms.CharField(max_length=25, label='Repetir contraseña',widget=forms.PasswordInput(attrs={'class': 'validate'}))
	apellido = forms.CharField(max_length=25, label='Apellido', widget=forms.TextInput(attrs={'class' : 'validate'}))
	nombre = forms.CharField(max_length=25, label='Nombre', widget=forms.TextInput(attrs={'class' : 'validate'}))