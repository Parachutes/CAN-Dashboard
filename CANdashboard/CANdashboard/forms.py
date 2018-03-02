from django import forms
from django.forms import ModelForm

from forms_builder.forms.models import FormManager,Form, FormEntry, FieldEntry, AbstractForm, Field
from forms_builder.forms.views import FormDetail
from forms_builder.forms.forms import EntriesForm,FormForForm


class allField(forms.ModelForm):

    class Meta:
        model = Field
        exclude = ('slug','form')


class addSurvey(forms.ModelForm):
    fieldentry_model = FieldEntry

    class Meta:
        model = FormEntry
        exclude = ('slug',)

class Description(forms.ModelForm):
    class Meta:
        model = Form
        exclude = ('slug','sites','redirect_url','email_from','response')
