from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Charity, User
from django.contrib.auth.decorators import login_required
from directmessages.apps import Inbox



def index(request):
    context = {}
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render(context, request))

def indexUser(request):
    context = {}
    template = loader.get_template('app/indexUser.html')
    return HttpResponse(template.render(context, request))
#
# def indexAdmin(request):
#     context = {}
#     template = loader.get_template('app/indexAdmin.html')
#     return HttpResponse(template.render(context, request))

# def indexTest(request):
#     context = {}
#     template = loader.get_template('app/indexBackUp.html')
#     return HttpResponse(template.render(context, request))



def Charity_detail(request,Name):
        charity = Charity.objects.filter(slug=Name)
        template = loader.get_template('app/index.html')
        return render(request,'app/index.html',{'charity': charity})


@login_required
def list_messages(request):
    user = User.objects.get(username=request.user.username)
    messages = Inbox.get_unread_messages(user).values_list('content',flat=True)
    return render(request,'app/inboxUser.html',{'messages': messages})


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
