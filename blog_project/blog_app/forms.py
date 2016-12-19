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
