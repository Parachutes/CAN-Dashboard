from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Charity, User
from django.contrib.auth.decorators import login_required
from directmessages.apps import Inbox
from directmessages.models import Message

from forms_builder.forms.models import FormManager,Form, FormEntry, FieldEntry, AbstractForm
from forms_builder.forms.views import FormDetail
from forms_builder.forms.forms import EntriesForm,FormForForm


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
    messages = Message.objects.all()
    mes = {
    "lk": messages
}
    return render(request,'app/inboxUser.html',mes)

def list_charity(request):
    chairities = Charity.objects.all().values_list('Name',flat=True)
    html = "<html><body>It is now %s.</body></html>" %chairities
    return HttpResponse(html)



def list_survey(request):
    surveys = Form.objects.all().values_list('title',flat=True)
    html = "<html><body>It is now %s.</body></html>" %surveys
    return HttpResponse(html)

def add_survey(request):
    form = FormDetail()
    return render(request,'app/index.html',{'form': form})



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
