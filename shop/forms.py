from django import forms

from shop.models import *


class OrderForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    quantity = forms.IntegerField()


# class CommentForm(forms.Form):
#     name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('slug', )


