from django import forms

class UserForm(forms.Form):
    username = forms.CharField(max_length=200)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(render_value = True))