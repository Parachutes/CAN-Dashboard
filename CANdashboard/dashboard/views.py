from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from .models import Charity, User, Charity_details
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from directmessages.apps import Inbox
from directmessages.models import Message
from CANdashboard.forms import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic.edit import FormView
from django.views.generic import UpdateView
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.core import serializers
from directmessages.signals import message_read, message_sent



from forms_builder.forms.models import FormManager,Form, FormEntry, FieldEntry, AbstractForm
from forms_builder.forms.views import FormDetail
from forms_builder.forms.forms import EntriesForm,FormForForm


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],email=form.cleaned_data['email'])
            #user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            #login(request, user)
            charity = Charity.objects.create(user=user,Name= user.username, slug=user.username)
            charity_detail = Charity_details.objects.create(Name=charity)
            return render(request,'app/indexAdmin.html')
    form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/signUp.html',variables)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfile(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            context = {}
            if not request.user.is_superuser:
                template = loader.get_template('app/indexAdmin.html')
                return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('app/indexUser.html')
                return HttpResponse(template.render(context, request))
    else :
        form = EditProfile(instance=request.user)
        if not request.user.is_superuser:
            return render(request,'app/charity_form.html',{'form':form})
        else:
            return render(request,'app/admin_form.html',{'form':form})



@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user = request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            context = {}
            if not user.is_superuser:
                template = loader.get_template('app/indexUser.html')
                return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('app/indexAdmin.html')
                return HttpResponse(template.render(context, request))
        else:
            form = PasswordChangeForm(user=request.user)
            if not user.is_superuser:
                return render (request,'app/changepassword.html',{'form':form})
            else:
                return render (request,'app/changepasswordAdmin.html',{'form':form})
    else :
        form = PasswordChangeForm(user=request.user)
        if not user.is_superuser:
            return render (request,'app/changepassword.html',{'form':form})
        else:
            return render (request,'app/changepasswordAdmin.html',{'form':form})


@login_required
class UpdateCharity(UpdateView):
    model = Charity
    fields = ['Name','Country','Website','Email']
    template_name = 'app/charity_form.html'

def index(request):
    user = User.objects.filter(username='Evain')
    charity = Charity.objects.get(user=user)
    char = Charity_details.objects.get(Name=charity)
    return render(request,'app/index.html',{'char':char})

@login_required
def indexUser(request):
    user = User.objects.filter(username='Evain')
    charity = Charity.objects.get(user=user)
    Charity_detail = Charity_details.objects.get(Name=charity)
    return render(request,'app/indexUser.html',{'Charity_detail':Charity_detail})


@login_required
def indexAdmin(request):
    user = User.objects.filter(username='Evain')
    charity = Charity.objects.get(user=user)
    Charity_detail = Charity_details.objects.get(Name=charity)

    return render(request,'app/indexAdmin.html',{'Charity_detail':Charity_detail})



#@login_required
# def Charity_detail(request,*args,**kwargs):
#     user = User.objects.filter(username='Evain')
#     charity = Charity.objects.get(user=user)
#     Charity_detail = Charity_details.objects.get(Name=charity)
#     #return JsonResponse(data)
#     #return JsonResponse(serializers.serialize('json', user),safe=False)
#     return render(request,'app/chart.html',{'Charity_detail':Charity_detail})


@login_required
def list_messages(request):
    user = User.objects.get(username=request.user.username)
    messages = SurveyMessage.objects.filter(recipient=user)
    mes = {
    "lk": messages
}
    if user.is_superuser:
        return render(request,'app/inboxAdmin.html',mes)
    else:
        return render(request,'app/inboxUser.html',mes)

# TODO Adueince View
def list_charity(request):
    charity = Charity.objects.all()
    chars = {
    "charity": charity
}
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return render(request,'app/charities_listAdmin.html',chars)
        else:
            return render(request,'app/charities_listUser.html',chars)
    else:
        return render(request,'app/charities_list.html',chars)


def loginAdmin(request):
    context = {}
    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    if user.is_superuser:
                        login(request, user)
                        template = loader.get_template('app/indexAdmin.html')
                        return HttpResponse(template.render(context, request))
                    else:
                        template = loader.get_template('registration/loginAdmin.html')
                        return HttpResponse(template.render(context, request))
                else:
                    template = loader.get_template('registration/loginAdmin.html')
                    return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('registration/loginAdmin.html')
                return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('registration/loginAdmin.html')
        return HttpResponse(template.render(context, request))


def survey_view(request,slug):
    question = Form.objects.get(slug=slug)
    form_for_form = FormForForm(question, RequestContext(request),
                                    request.POST or None,
                                    request.FILES or None)
    return render(request,'app/view_survey.html',{'form_for_form':form_for_form,'question':question})


def bla(request):
    ma = Form.objects.all().values_list('slug',flat=True)
    html = "<html><body>It is now %s.</body></html>" %ma
    return HttpResponse(html)


def list_survey(request):
    surveys = Form.objects.all()
    surv = {
        "survey": surveys
    }
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return render(request,'app/survey_squareAdmin.html',surv)
        else:
            return render(request,'app/survey_squareUser.html',surv)
    else:
        return render(request,'app/survey_square.html',surv)

def add_survey(request):
    allFiel = allField()
    fields = addSurvey() ## UNNESSECARYY
    form = Description()
    return render(request,'app/add_survey.html',{'form': form,'fields':fields,'allFiel':allFiel})

@login_required
def send_message(request):
    user = request.user
    if request.method == 'POST':
        form = SendMessage(request.POST)
        if form.is_valid():
            message = SurveyMessage(sender=user,recipient=form.cleaned_data['recipient'],content=form.cleaned_data['content'],survey=form.cleaned_data['survey'])
            message.save()
            message_sent.send(sender= message,from_user=message.sender,to=message.recipient)
            if user.is_superuser:
                return render(request,'app/indexAdmin.html')
            else:
                return render(request,'app/indexUser.html')
        else:
            if not user.is_superuser:
                return render(request,'app/send_message.html')
            else:
                return render(request,'app/send_messageAdmin.html')
    else:
        form = SendMessage()
        variables = RequestContext(request, {'form': form})
        if not user.is_superuser:
            return render_to_response('app/send_message.html',variables)
        else:
            return render_to_response('app/send_messageAdmin.html',variables)




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
