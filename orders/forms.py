from django import forms
from .models import Order
from django.forms import Textarea


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code',
                  'city', 'comment']
        widgets = {
				 'commet' : Textarea(attrs={'cols': 80, 'rows': 20}),
				}