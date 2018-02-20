from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Charity, User



def index(request):
    context = {}
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render(context, request))

def indexUser(request):
    context = {}
    template = loader.get_template('app/indexUser.html')
    return HttpResponse(template.render(context, request))

def indexAdmin(request):
    context = {}
    template = loader.get_template('app/indexAdmin.html')
    return HttpResponse(template.render(context, request))

def indexTest(request):
    context = {}
    template = loader.get_template('app/indexBackUp.html')
    return HttpResponse(template.render(context, request))


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))

def Charity_detail(request,Name):
        charity = Charity.objects.filter(slug=Name)
        template = loader.get_template('app/index.html')
        return render(request,'app/index.html',{'charity': charity})
