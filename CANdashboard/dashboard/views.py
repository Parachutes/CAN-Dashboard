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

        

#TODO request username for list messages from login
#def list_messages(request):
#    touser =User.objects.get(username ='ALS')
#    touser.username = touser
#    mes = Inbox.get_unread_messages(touser).values_list('content',flat=True)
#    html = "<html><body>It is now %s.</body></html>" % mes
#    return HttpResponse(html)

# TODO request other charity name and obtain from_user from login
#def send_message(request):
    #user =User.objects.get(username ='zaki')
    #user.username = user
    #touser =User.objects.get(username ='ALS')
    #touser.username = touser
    #message = 'Hello'
    #Inbox.send_message(user, touser, message)
    #html = "<html><body>It is now %s.</body></html>" %message
    #return HttpResponse(html)
