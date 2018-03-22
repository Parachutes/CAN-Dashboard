from django import forms
from django.forms import ModelForm
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from dashboard.models import *
from dashboard.views import *
from django.contrib.auth.forms import UserChangeForm
from django.forms.models import modelformset_factory, formset_factory
from django.forms import BaseFormSet
from forms_builder.forms.models import FormManager,Form, FormEntry, FieldEntry, AbstractForm, Field
from forms_builder.forms.views import FormDetail
from forms_builder.forms.forms import EntriesForm,FormForForm
from django.forms import fields, models, formsets, widgets


# class UpdateUser(forms.Form):
#     class Meta:
#         model = UpdateCharity
#

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password',
                          widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password (Again)',
                        widget=forms.PasswordInput())
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')

class EditProfile(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password')


class allField(forms.ModelForm):

    class Meta:
        model = QuestionMarks
        exclude = ('slug','form')


class addSurvey(forms.ModelForm):
    class Meta:
        model = FormEntry
        exclude = ('slug',)

class relatedSurvey(forms.ModelForm):
    class Meta:
        model = RelatedSurvey
        exclude = ('question',)

class Description(forms.ModelForm):
    class Meta:
        model = Form
        exclude = ('slug','sites','redirect_url','email_from','response')


class SendMessage(forms.ModelForm):
    class Meta:
        model = SurveyMessage
        exclude = ('slug','sender','sent_at','read_at')
