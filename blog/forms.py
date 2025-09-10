from django import forms 

class SigninForm(forms.Form):
    first_name = forms.CharField(required=True, label="Type your first name")
    last_name = forms.CharField(required=False, label="Type your last name")
    email = forms.EmailField(label="Type your email")
    password = forms.CharField(widget=forms.PasswordInput(), label="Type your password")
    
class LoginForm(forms.Form):
    email = forms.EmailField(label="Type your email", required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput(), label="Type your password")
    