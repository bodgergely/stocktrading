from django import forms

class QueryForm(forms.Form):
	stock_symbol = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label='Stock symbol', max_length=100, required=True)

class PurchaseForm(forms.Form):
	stock_symbol = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label='Stock symbol', max_length=100, required=True)
	quantity = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label='Quantity', max_length=10, required=True)
	
class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label='Username', max_length=100, required=True)
	password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), label='Password', max_length=100, required=True)
	remember = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "checkbox"}), label="Remember me", required=False)

class RegisterForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label='Username', max_length=100, required=True)
	password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), label='Password', max_length=100, required=True)
	password_conf = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), label='Password Again', max_length=100, required=True)
	email_address = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control"}) ,label='Email', max_length=100, required=True)