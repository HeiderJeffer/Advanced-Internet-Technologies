from django import forms
from django.core import validators
from django.contrib.auth import get_user_model
from . import models

class UserForm(forms.Form):
    username = forms.CharField(widget = forms.TextInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'e.g johndoe',
            'pattern': '[A-Za-z0-9_]{3,20}',
            'title': 'alphanumeric symbols or underscore between 3 and 20 characters'
        })
    )
    first_name = forms.CharField(widget = forms.TextInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'e.g. John',
            'pattern': '([^\s][A-zÀ-ž\s]+)',
            'title': 'Alphabet symbols and spaces only'
        }))
    last_name = forms.CharField(widget = forms.TextInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'e.g. Doe',
            'pattern': '([^\s][A-zÀ-ž\s]+)',
            'title': 'Alphabet symbols and spaces only'
        }))
    email = forms.EmailField(widget = forms.EmailInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'e.g. johndoe@gmail.com',
        }))
    email_repeat = forms.EmailField(widget = forms.EmailInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'e.g. johndoe@gmail.com',
        }))
    password = forms.CharField(widget = forms.PasswordInput(attrs = {
        'class' : 'form-control',
    }))
    password_repeat = forms.CharField(widget = forms.PasswordInput(attrs = {
        'class' : 'form-control',
    }))
    address = forms.CharField(max_length = 264, required = False, widget = forms.TextInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'e.g. Embassy of Ecuador, London',
        }))
    phone = forms.CharField(max_length = 20, required = False, widget = forms.TextInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'e.g. 555 555 555 555',
        }))
    botcatcher = forms.CharField(required = False, widget = forms.HiddenInput)  #this is to catch bots: hidden field, so actual user won't fill it, bot will

    def clean(self):
        clean_data = super().clean()
        botcatcher = clean_data['botcatcher']
        if len(botcatcher) > 0:
            raise forms.ValidationError("Bot caught")
        if clean_data['email']!=clean_data['email_repeat']:
            raise forms.ValidationError("Emails don't match")
        if clean_data['password']!=clean_data['password_repeat']:
            raise forms.ValidationError("Passwords don't match")

    # def clean_botcatcher(self):  #custom validator
    #     botcatcher = self.cleaned_data['botcatcher']
    #     if len(botcatcher) > 0:
    #         raise forms.ValidationError("Bot caught")
    #     return botcatcher


class UserEditForm(forms.ModelForm):

    class Meta():
        fields = ('first_name','last_name')
        model = get_user_model()
        widgets = {

                'first_name' : forms.TextInput(
                        attrs = {
                            'class' : 'form-control',
                            'placeholder' : 'e.g. John',
                            'pattern': '([^\s][A-zÀ-ž\s]+)',
                            'title': 'Alphabet symbols and spaces only'
                        }),
                'last_name' : forms.TextInput(
                        attrs = {
                            'class' : 'form-control',
                            'placeholder' : 'e.g. Doe',
                            'pattern': '([^\s][A-zÀ-ž\s]+)',
                            'title': 'Alphabet symbols and spaces only'
                        }),                
        }


class ProfileEditForm(forms.ModelForm):
    class Meta():
        model = models.UserProfile
        fields =  ('phone','address')
        widgets = {
            'phone': forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : 'e.g. 555 555 555 555',
                }),
            'address' : forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : 'e.g. Embassy of Ecuador, London',
                }),

        }
