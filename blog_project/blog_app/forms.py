# -*- coding: utf-8 -*-
from django import forms
from .models import Comment
class Comment_form(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content', 'username', 'email', 'url', 'user', 'article'] 
	url = forms.URLField(widget=forms.TextInput(attrs={"id":"url","type":"url","class": "comment_input",
                                                       "size":"25", "tabindex":"3"}),
                              max_length=100, required=False)

class Reg_Form(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username','required':'required'}), max_length=50, error_messages={"required": "username不能为空",})
	email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'email', 'required':'required'}), max_length=50, error_messages={'required':'email不能为空'})
	url = forms.URLField(widget=forms.URLInput(attrs={'placeholder':'url',}), max_length=100, required=False)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password', 'required':'required'}), max_length=20, error_messages={'required':'passworld不能为空'})

class Login_Form(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username','required':'required'}), max_length=50, error_messages={"required": "username不能为空",})
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password', 'required':'required'}), max_length=20, error_messages={'required':'passworld不能为空'})
