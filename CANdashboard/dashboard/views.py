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
import forms_builder.forms.views
from forms_builder.forms.forms import EntriesForm,FormForForm


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password2'],email=form.cleaned_data['email'])
            #user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            #user.backend = 'django.contrib.auth.backends.ModelBackend'
            #login(request, user)
            charity = Charity.objects.create(user=user,Name= user.username, slug=user.username)
            charity_detail = Charity_details.objects.create(Name=charity)
            return render(request,'app/indexAdmin.html')
        else:
            form = RegistrationForm(request.POST)
            return render (request,'registration/signUp.html',{'form':form})
    else :
        form = RegistrationForm()
        return render (request,'registration/signUp.html',{'form':form})

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



def Charity_detail(request,Name):
    user = User.objects.get(username=Name)
    charity = Charity.objects.get(user=user)
    Charity_detail = Charity_details.objects.get(Name=charity)
    #html = "<html><body>It is now %s.</body></html>" %Charity_detail
    if user.is_authenticated:
        if user.is_superuser:
            return render(request,'app/indexAdmin.html',{'Charity_detail':Charity_detail})
        else:
            return render(request,'app/indexUser.html',{'Charity_detail':Charity_detail})
    else:
        return render(request,'app/index.html',{'Charity_detail':Charity_detail})


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


def Manipulate_Entries(request):
    ma = Form.objects.get(slug='shichaos-quiz')
    formentry = FormEntry.objects.get(form = ma)

    form = FieldEntry.objects.filter(entry_id = formentry)
    entry = EntriesForm(ma,RequestContext(request),formentry,form,request.POST or None)
    questions = ma.fields.all()
    return render(request,'app/man_entries.html',{'entry':entry,'form':form,'questions':questions})


def DeliveryCategory(request):
    ma = Form.objects.get(slug='shichaos-quiz')
    questions = ma.fields.all()
    formentry = FormEntry.objects.get(form = ma)
    form = FieldEntry.objects.filter(entry_id = formentry)
    survey = RelatedSurvey.objects.filter(category=RelatedSurvey.Delivery)
    return render(request,'app/DeliveryPage.html',{'questions':questions,'form':form,'survey':survey})


def FinancialCategory(request):
    survey = RelatedSurvey.objects.filter(category=RelatedSurvey.Financial_Health)
    return render(request,'app/FinancialPage.html',{'survey':survey})

def StrengthCategory(request):
    survey = RelatedSurvey.objects.filter(category=RelatedSurvey.Strength_of_system)
    return render(request,'app/StrengthPage.html',{'survey':survey})

def ProgressCategory(request):
    survey = RelatedSurvey.objects.filter(category=RelatedSurvey.Progress)
    return render(request,'app/ProgressPage.html',{'survey':survey})

def surveyAnalysis(request,id):
    survey = Form.objects.get(id=id)
    questions = survey.fields.all()
    formentry = FormEntry.objects.filter(form = survey)
    entries = FieldEntry.objects.filter(entry_id = formentry)
    return render(request, 'app/surveyAnalysis.html',{'questions':questions,'entries':entries,'survey':survey})



def DeleteEntry(request, id):
    ma = Form.objects.get(slug='shichaos-quiz')
    entry = FormEntry.objects.filter(form = ma).values_list('id',flat=True)
    #entry = FieldEntry.objects.filter(entry_id=id).delete()
    html = "<html><body>It is now %s.</body></html>" %entry

    return HttpResponse(html)

def getsurv(request):
    # form = Form.objects.get(slug='first')
    # newQ = RelatedSurvey(question=form,category="Delivery")
    # newQ.save()
    question = RelatedSurvey.objects.filter(category=RelatedSurvey.Delivery).values_list('question',flat=True)
    return render(request,'app/bla.html',{'question':question})


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
        if not user.is_superuser:
            return render(request,'app/send_message.html',{'form':form})
        else:
            return render(request,'app/send_messageAdmin.html',{'form':form})





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
