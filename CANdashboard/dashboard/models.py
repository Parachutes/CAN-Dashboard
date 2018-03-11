from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from forms_builder.forms.models import FormManager,Form, FormEntry, FieldEntry, AbstractForm,Field
from directmessages.models import Message

class Charity(models.Model):
    user = models.ForeignKey(User)
    Name = models.CharField(max_length=80)
    Country = models.CharField(max_length=20, blank=True)
    Website = models.URLField(blank=True,default = '')
    Email = models.EmailField(blank=True,default = '')
    slug = models.SlugField(max_length=200, unique=True)
    prepopulated_fields = { 'slug': ['Name']}

    class Meta:
        ordering = ('Name',)
        verbose_name = 'Charity'
        verbose_name_plural = 'Charities'

    def __str__(self):
        return self.Name

class Charity_details(models.Model):
    Name = models.ForeignKey(Charity)
    Delivery = models.IntegerField(blank=True, default = '0')   #1
    Financial_health = models.IntegerField(blank=True, default = '0')   #2
    Strength_of_system = models.IntegerField(blank=True, default = '0') #3
    Progress = models.IntegerField(blank=True, default = '0')   #4

def get_absolute_url(self):
    return reverse('Charity:Charity_details',args=[self.slug])

class RelatedQuestion(models.Model):
    question = models.ForeignKey(Field)
    category = models.ForeignKey(Charity_details)

class SurveyMessage(Message):
    survey = models.ForeignKey(Form)
