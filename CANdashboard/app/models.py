from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm
from django.core.urlresolvers import reverse


class Charity(models.Model):
    Name = models.CharField(max_length=80)
    Country = models.CharField(max_length=20)
    Website = models.URLField()
    Email = models.EmailField(primary_key=True)
    slug = models.SlugField(max_length=200, unique=True)

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

class Response(models.Model):
    Name = models.ForeignKey(Charity_details)
    Response = models.FloatField()
    Field = models.IntegerField()

def get_absolute_url(self):
    return reverse('Charity:Charity_details',args=[self.slug])
