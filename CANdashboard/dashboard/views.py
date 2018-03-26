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
from django.forms import formset_factory, modelformset_factory
from django.views import View
from forms_builder.forms.signals import form_invalid, form_valid
from forms_builder.forms.utils import now, split_choices
from more_itertools import chunked
from statistics import mean
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages




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


def getCharityNameforSurvey(forms):
    # forms = Form.objects.get(id=forms.id)
    # #fields = QuestionMarks.objects.filter(form=forms)
    # entrie = forms.entries.all()
    charityName = None
    answers = None

    answers = FieldEntry.objects.filter(entry = forms).values_list('value',flat=True)


    for index,field in enumerate(answers):
            if index==0:
                charityName = str(field)


    return charityName




def calculteTotalMark(forms):
        entries = FormEntry.objects.filter(form = forms)
        entryAnswers = entries.all()
        answers = []
        Total = 0
        avgCategory = 0

        for a in entryAnswers:
            answers.append(list(FieldEntry.objects.filter(entry = a).values_list('value',flat=True)))

        forms = Form.objects.get(id=forms.id)
        questions = forms.fields.all()
        entrie = forms.entries.all()
        fields = QuestionMarks.objects.filter(form=forms)
        choices = []
        entryFields = []
        marks = []
        marking = []
        indexs = []

        for entry in entrie:
            entryFields.append(list(FieldEntry.objects.filter(entry=entry).values_list('value',flat=True)))

        for  indx,mark in enumerate(fields):
            if indx == 1:
                pass
            else:
                marks.append((list(mark.get_marks())))
                choices.append(list(mark.get_choices()))

        for e in entryFields:
            for entry in e:
                for choice in choices:
                    if entry in choice:
                        indexs.append(choice.index(entry))



        for i in indexs:
            for mark in marks:
                try:
                    marking.append(int(mark[i]))
                except IndexError:
                    marking.append(0)


        cele = list(chunked(marking, len(questions)))
        totalEntryMark = map(sum,cele)
        individualQMark = list(chunked(marking, len(questions)))
        weightedEntry = zip(entryFields,individualQMark)



        for ex in totalEntryMark:
            Total += ex

        if len(individualQMark) == 0:
            return Total
        else:
            return Total/len(individualQMark)

def index(request):
    ProgressSurveys = RelatedSurvey.objects.filter(category='Progress')
    DeliverySurveys = RelatedSurvey.objects.filter(category='Delivery')
    StrengthSurveys = RelatedSurvey.objects.filter(category='Strength_of_system')
    FinancialSurveys = RelatedSurvey.objects.filter(category='Financial_Health')

    Progressmarks = []
    totalProgressMark = 0
    avgProgress = 0
    Deliverymarks = []
    totalDeliverymarks = 0
    avgDelivery = 0
    Strengthmarks = []
    totalStrengthmarks = 0
    avgStrength = 0
    Healthmarks = []
    totalHealthmarks = 0
    avgHealth = 0


    for p in ProgressSurveys:
        Progressmarks.append(calculteTotalMark(p.question))

    for d in DeliverySurveys:
        Deliverymarks.append(calculteTotalMark(d.question))

    for s in StrengthSurveys:
        Strengthmarks.append(calculteTotalMark(s.question))

    for h in FinancialSurveys:
        Healthmarks.append(calculteTotalMark(h.question))


    for Pmark in Progressmarks:
        if Pmark  == None:
            pass
        else:
            totalProgressMark += Pmark
        if len(ProgressSurveys) == 0:
            avgProgress = totalProgressMark
        else:
            avgProgress = format(totalProgressMark / len(ProgressSurveys), '.2f')

    for Dmark in Deliverymarks:
        if Dmark == None:
            pass
        else:
            totalDeliverymarks += Dmark
        if len(Deliverymarks) == 0:
            avgDelivery = totalDeliverymarks
        else:
            avgDelivery = format(totalDeliverymarks / len(Deliverymarks), '.2f')

    for Smark in Strengthmarks:
        if Smark == None:
            pass
        else:
            totalStrengthmarks += Smark
        if len(Strengthmarks) == 0:
            avgStrength = totalStrengthmarks
        else:
            avgStrength = format(totalStrengthmarks / len(Strengthmarks), '.2f')

    for Hmark in Healthmarks:
        if Hmark == None:
            pass
        else:
            totalHealthmarks += Hmark
        if len(Healthmarks) == 0:
            avgHealth = totalHealthmarks
        else:
            avgHealth = format(totalHealthmarks / len(Healthmarks), '.2f')

    return render(request,'app/index.html',locals())

@login_required
def indexUser(request):
    user = request.user
    ProgressSurveys = RelatedSurvey.objects.filter(category='Progress')
    DeliverySurveys = RelatedSurvey.objects.filter(category='Delivery')
    StrengthSurveys = RelatedSurvey.objects.filter(category='Strength_of_system')
    FinancialSurveys = RelatedSurvey.objects.filter(category='Financial_Health')

    Progressmarks = []
    totalProgressMark = 0
    avgProgress = 0
    ProgressEntries = []
    Deliverymarks = []
    totalDeliverymarks = 0
    avgDelivery = 0
    DeliveryEntries = []
    Strengthmarks = []
    totalStrengthmarks = 0
    avgStrength = 0
    StrengthEntries = []
    Healthmarks = []
    totalHealthmarks = 0
    avgHealth = 0
    HealthEntries = []
    totalDeliveryEntry = 0
    totalStrengthEntry = 0
    totalProgressEntry = 0
    totalHealthEntry = 0


    for p in ProgressSurveys:
        for pr in p.question.entries.all():
            if request.user.username != getCharityNameforSurvey(pr):
                pass
            else:
                Progressmarks.append(calculteTotalMark(p.question))

    for d in DeliverySurveys:
        for dr in d.question.entries.all():
            if request.user.username != getCharityNameforSurvey(dr):
                pass
            else:
                Deliverymarks.append(calculteTotalMark(d.question))

    for s in StrengthSurveys:
        for sr in s.question.entries.all():
            if request.user.username != getCharityNameforSurvey(sr):
                pass
            else:
                Strengthmarks.append(calculteTotalMark(s.question))

    for h in FinancialSurveys:
        for fr in h.question.entries.all():
            if request.user.username != getCharityNameforSurvey(fr):
                pass
            else:
                Healthmarks.append(calculteTotalMark(h.question))


    for Pmark in Progressmarks:
        if Pmark  == None:
            pass
        else:
            totalProgressMark += Pmark
        if len(ProgressSurveys) == 0:
            avgProgress = totalProgressMark
        else:
            avgProgress = format(totalProgressMark / len(ProgressSurveys), '.2f')

    for Dmark in Deliverymarks:
        if Dmark == None:
            pass
        else:
            totalDeliverymarks += Dmark
        if len(Deliverymarks) == 0:
            avgDelivery = totalDeliverymarks
        else:
            avgDelivery = format(totalDeliverymarks / len(Deliverymarks), '.2f')

    for Smark in Strengthmarks:
        if Smark == None:
            pass
        else:
            totalStrengthmarks += Smark
        if len(Strengthmarks) == 0:
            avgStrength = totalStrengthmarks
        else:
            avgStrength = format(totalStrengthmarks / len(Strengthmarks), '.2f')

    for Hmark in Healthmarks:
        if Hmark == None:
            pass
        else:
            totalHealthmarks += Hmark
        if len(Healthmarks) == 0:
            avgHealth = totalHealthmarks
        else:
            avgHealth = format(totalHealthmarks / len(Healthmarks), '.2f')

    for ss in StrengthSurveys:
        for x in ss.question.entries.all():
            if str(user) != getCharityNameforSurvey(x):
                pass
            else:
                StrengthEntries.append(len(FieldEntry.objects.filter(entry=x)))


    for ds in DeliverySurveys:
        for o in ds.question.entries.all():
            if request.user.username != getCharityNameforSurvey(o):
                pass
            else:
                DeliveryEntries.append(len(FieldEntry.objects.filter(entry=o)))

    for fs in FinancialSurveys:
        for m in fs.question.entries.all():
            if request.user.username != getCharityNameforSurvey(m):
                pass
            else:
                HealthEntries.append(len(FieldEntry.objects.filter(entry=m)))

    for ps in FinancialSurveys:
        for l in ps.question.entries.all():
            if request.user.username  != getCharityNameforSurvey(l):
                pass
            else:
                ProgressEntries.append(len(FieldEntry.objects.filter(entry=l)))

    for delivery in DeliveryEntries:
        totalDeliveryEntry += delivery

    for health in HealthEntries:
        totalHealthEntry += health

    for strength in StrengthEntries:
        totalStrengthEntry += strength

    for progress in ProgressEntries:
        totalProgressEntry += progress


    print(totalHealthmarks,totalDeliverymarks,totalProgressMark,totalStrengthmarks)

    CategorisedEntries = []

    CategorisedEntries.append((RelatedSurvey.Progress,totalProgressEntry))
    CategorisedEntries.append((RelatedSurvey.Strength_of_system,totalStrengthEntry))
    CategorisedEntries.append((RelatedSurvey.Financial_Health,totalHealthEntry))
    CategorisedEntries.append((RelatedSurvey.Delivery,totalDeliveryEntry))


    return render(request,'app/indexUser.html',locals())


@login_required
def indexAdmin(request):
    ProgressSurveys = RelatedSurvey.objects.filter(category='Progress')
    DeliverySurveys = RelatedSurvey.objects.filter(category='Delivery')
    StrengthSurveys = RelatedSurvey.objects.filter(category='Strength_of_system')
    FinancialSurveys = RelatedSurvey.objects.filter(category='Financial_Health')

    Progressmarks = []
    totalProgressMark = 0
    avgProgress = 0
    ProgressEntries = []
    Deliverymarks = []
    totalDeliverymarks = 0
    avgDelivery = 0
    DeliveryEntries = []
    Strengthmarks = []
    totalStrengthmarks = 0
    avgStrength = 0
    StrengthEntries = []
    Healthmarks = []
    totalHealthmarks = 0
    avgHealth = 0
    HealthEntries = []
    totalDeliveryEntry = 0
    totalStrengthEntry = 0
    totalProgressEntry = 0
    totalHealthEntry = 0


    for p in ProgressSurveys:
        Progressmarks.append(calculteTotalMark(p.question))
        ProgressEntries.append(len(FormEntry.objects.filter(form=p.question)))


    for d in DeliverySurveys:
        Deliverymarks.append(calculteTotalMark(d.question))
        DeliveryEntries.append(len(FormEntry.objects.filter(form=p.question)))

    for s in StrengthSurveys:
        Strengthmarks.append(calculteTotalMark(s.question))
        StrengthEntries.append(len(FormEntry.objects.filter(form=p.question)))

    for h in FinancialSurveys:
        Healthmarks.append(calculteTotalMark(h.question))
        HealthEntries.append(len(FormEntry.objects.filter(form=p.question)))


    for Pmark in Progressmarks:
        if Pmark  == None:
            pass
        else:
            totalProgressMark += Pmark
        if len(ProgressSurveys) == 0:
            avgProgress = totalProgressMark
        else:
            avgProgress = format(totalProgressMark / len(ProgressSurveys), '.2f')

    for Dmark in Deliverymarks:
        if Dmark == None:
            pass
        else:
            totalDeliverymarks += Dmark
        if len(Deliverymarks) == 0:
            avgDelivery = totalDeliverymarks
        else:
            avgDelivery = format(totalDeliverymarks / len(Deliverymarks), '.2f')

    for Smark in Strengthmarks:
        if Smark == None:
            pass
        else:
            totalStrengthmarks += Smark
        if len(Strengthmarks) == 0:
            avgStrength = totalStrengthmarks
        else:
            avgStrength = format(totalStrengthmarks / len(Strengthmarks), '.2f')

    for Hmark in Healthmarks:
        if Hmark == None:
            pass
        else:
            totalHealthmarks += Hmark
        if len(Healthmarks) == 0:
            avgHealth = totalHealthmarks
        else:
            avgHealth = format(totalHealthmarks / len(Healthmarks), '.2f')

    for delivery in DeliveryEntries:
        totalDeliveryEntry += delivery

    for health in HealthEntries:
        totalHealthEntry += health

    for strength in StrengthEntries:
        totalStrengthEntry += strength

    for progress in ProgressEntries:
        totalProgressEntry += progress


    CategorisedEntries = []

    CategorisedEntries.append((RelatedSurvey.Progress,totalProgressEntry))
    CategorisedEntries.append((RelatedSurvey.Strength_of_system,totalStrengthEntry))
    CategorisedEntries.append((RelatedSurvey.Financial_Health,totalHealthEntry))
    CategorisedEntries.append((RelatedSurvey.Delivery,totalDeliveryEntry))


    return render(request,'app/indexAdmin.html',locals())



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
                        template = 'app/indexAdmin.html'
                        return HttpResponseRedirect(reverse('AdminProfile'))
                    else:
                        template = 'registration/loginAdmin.html'
                        return render(request,template)
                else:
                    template = 'registration/loginAdmin.html'
                    return render(request,template)
            else:
                template = 'registration/loginAdmin.html'
                return render(request,template)
    else:
        template = 'registration/loginAdmin.html'
        return render(request,template)



class SurveyDetail(FormDetail):
    template_name = "app/view_survey.html"


def Manipulate_Entries(request,slug):
    user = request.user
    ma = Form.objects.get(slug=slug)
    questions = ma.fields.all()
    formentry = FormEntry.objects.filter(form = ma)[:1].get()
    form = FieldEntry.objects.filter(entry_id = formentry)
    entryTable = EntriesForm(ma,RequestContext(request),formentry,form,request.POST or None)

    entries = FormEntry.objects.filter(form = ma)
    entryAnswers = entries.all()
    answers = []

    for a in entryAnswers:
        answers.append(list(FieldEntry.objects.filter(entry = a).values_list('value',flat=True)))

    forms = Form.objects.get(slug=slug)
    questions = forms.fields.all()
    unfilteredentrie = forms.entries.all()
    fields = QuestionMarks.objects.filter(form=forms)
    choices = []
    entryFields = []
    marks = []
    marking = []
    indexs = []
    entrie = []

    for entry in unfilteredentrie:
        if request.user.username  != str(getCharityNameforSurvey(entry)):
            pass
        else:
            entrie.append(list(FieldEntry.objects.filter(entry = entry).values_list('value',flat=True)))

    for unfilentry in entrie:
        for index,unfilen in enumerate(unfilentry):
            if index == 0:
                unfilentry.pop(0)


    # for entry in entrie:
    #     entryFields.append(list(FieldEntry.objects.filter(entry=entry).values_list('value',flat=True)))

    for mark in fields:
        marks.append((list(mark.get_marks())))
        choices.append(list(mark.get_choices()))

    for e in entrie:
        for entry in e:
            for choice in choices:
                if entry in choice:
                    indexs.append(choice.index(entry))

    for i in indexs:
        for mark in marks:
            marking.append(int(mark[i]))

    cele = list(chunked(marking, len(questions)-1))
    totalEntryMark = map(sum,cele)

    for i in indexs:
        for mark in marks:
            marking.append(int(mark[i]))

    individualQMark = list(chunked(marking, len(questions)-1))
    weightedEntry = zip(entrie,individualQMark)


    return render(request,'app/man_entries.html',locals())


def DeliveryCategory(request):
    user = request.user
    survey = RelatedSurvey.objects.filter(category=RelatedSurvey.Delivery)
    DeliverySurveys = RelatedSurvey.objects.filter(category='Delivery')

    Deliverymarks = []
    surveyQuestions = []
    DeliveryEntries = []


    for d in DeliverySurveys:
        if len(d.question.entries.all()) != 0:
            for dr in d.question.entries.all():
                if request.user.username != getCharityNameforSurvey(dr):
                    continue
            Deliverymarks.append(format(calculteTotalMark(d.question)/len(d.question.entries.all()), '.2f'))
            surveyQuestions.append(d.question.title)
        else:
            for dr in d.question.entries.all():
                if request.user.username != getCharityNameforSurvey(dr):
                    continue
            Deliverymarks.append(calculteTotalMark(d.question))
            surveyQuestions.append(d.question.title)
        DeliveryEntries.append(len(FormEntry.objects.filter(form=d.question)))


    weightedSurvey = zip(surveyQuestions,Deliverymarks)
    numberOfEntries =  zip(surveyQuestions,DeliveryEntries)
    Surveys = zip(survey,DeliveryEntries)

    RadarSurveys = zip(surveyQuestions,Deliverymarks)
    marksurveys = zip(surveyQuestions,Deliverymarks)


    return render(request,'app/DeliveryPage.html',locals())


def FinancialCategory(request):
    user = request.user
    survey = RelatedSurvey.objects.filter(category=RelatedSurvey.Financial_Health)
    FinancialSurveys = RelatedSurvey.objects.filter(category='Financial_Health')

    Financialmarks = []
    surveyQuestions = []
    FinancialEntries = []



    for d in FinancialSurveys:
        if len(d.question.entries.all()) != 0:
            for fr in d.question.entries.all():
                if request.user.username != getCharityNameforSurvey(fr):
                    continue
            Financialmarks.append(format(calculteTotalMark(d.question)/len(d.question.entries.all()), '.2f'))
            surveyQuestions.append(d.question.title)
        else:
            for fr in d.question.entries.all():
                if request.user.username != getCharityNameforSurvey(fr):
                    continue
            Financialmarks.append(calculteTotalMark(d.question))
            surveyQuestions.append(d.question.title)

        FinancialEntries.append(len(FormEntry.objects.filter(form=d.question)))


    FinancialSurveys = zip(surveyQuestions,Financialmarks)
    numberOfEntries = zip(surveyQuestions,FinancialEntries)
    Surveys = zip(survey,FinancialEntries)

    RadarSurveys = zip(surveyQuestions,Financialmarks)
    marksurveys = zip(surveyQuestions,Financialmarks)
    return render(request,'app/FinancialPage.html',locals())

def StrengthCategory(request):
    user = request.user
    survey = RelatedSurvey.objects.filter(category=RelatedSurvey.Strength_of_system)
    StrengthSurveys = RelatedSurvey.objects.filter(category=RelatedSurvey.Strength_of_system)

    Strengthmarks = []
    surveyQuestions = []
    StrengthEntries = []


    for d in StrengthSurveys:
        if len(d.question.entries.all()) != 0:
            for dr in d.question.entries.all():
                if request.user.username != getCharityNameforSurvey(dr):
                    continue
            Strengthmarks.append(format(calculteTotalMark(d.question)/len(d.question.entries.all()), '.2f'))
            surveyQuestions.append(d.question.title)
        else:
            for dr in d.question.entries.all():
                if request.user.username != getCharityNameforSurvey(dr):
                    continue
            Strengthmarks.append(calculteTotalMark(d.question))
            surveyQuestions.append(d.question.title)
        StrengthEntries.append(len(FormEntry.objects.filter(form=d.question)))


    StrengthSurveys = zip(surveyQuestions,Strengthmarks)
    numberOfEntries = zip(surveyQuestions,StrengthEntries)
    Surveys = zip(survey,StrengthEntries)
    RadarSurveys = zip(surveyQuestions,Strengthmarks)
    marksurveys = zip(surveyQuestions,Strengthmarks)

    return render(request,'app/StrengthPage.html',locals())

def ProgressCategory(request):
    user = request.user
    survey = RelatedSurvey.objects.filter(category=RelatedSurvey.Progress)
    ProgressSurveys = RelatedSurvey.objects.filter(category='Progress')

    Progressmarks = []
    surveyQuestions = []
    ProgressEntries = []


    for d in ProgressSurveys:
        if len(d.question.entries.all()) != 0:
            for dr in d.question.entries.all():
                if request.user.username != getCharityNameforSurvey(dr):
                    continue
            Progressmarks.append(format(calculteTotalMark(d.question)/len(d.question.entries.all()), '.2f'))
            surveyQuestions.append(d.question.title)
        else:
            for dr in d.question.entries.all():
                if request.user.username != getCharityNameforSurvey(dr):
                    continue
            Progressmarks.append(calculteTotalMark(d.question))
            surveyQuestions.append(d.question.title)
        ProgressEntries.append(len(FormEntry.objects.filter(form=d.question)))




    ProgressSurveys = zip(surveyQuestions,Progressmarks)
    numberOfEntries = zip(surveyQuestions,ProgressEntries)
    Surveys = zip(survey,ProgressEntries)

    RadarSurveys = zip(surveyQuestions,Progressmarks)
    marksurveys = zip(surveyQuestions,Progressmarks)

    return render(request,'app/ProgressPage.html',locals())


def surveyAnalysis(request,id):
    user = request.user
    survey = Form.objects.get(id=id)
    unfilteredquestions = survey.fields.all()
    formentry = FormEntry.objects.filter(form = survey)
    # w = FieldEntry.objects.all().values_list('',flat=True)
    entries = []


    form = Form.objects.get(id=id)
    unfilteredentrie = form.entries.all()
    fields = QuestionMarks.objects.filter(form=form)
    choices = []
    entryFields = []
    marks = []
    marking = []
    indexs = []
    entrie = []
    questions = []
    questionsForm =[]

    for entry in unfilteredentrie:

        if request.user.username  != getCharityNameforSurvey(entry):
            pass
        else:
            entries.append(list(FieldEntry.objects.filter(entry = entry).values_list('value',flat=True)))

    for unfilentry in entries:
        for index,unfilen in enumerate(unfilentry):
            if index == 0:
                unfilentry.pop(0)


    for mark in fields:
        marks.append((list(mark.get_marks())))
        choices.append(list(mark.get_choices()))

    for e in entries:
        for index,entry in enumerate(e):
            if index == 0:
                pass
            else:
                for i,choice in enumerate(choices):
                    if i == 0:
                        pass
                    else:
                        if entry in choice:
                            indexs.append(choice.index(entry))

    for i in indexs:
        for mark in marks:
            marking.append(int(mark[i]))

    individualQMark = list(chunked(marking, len(fields)))
    totalEntryMark = map(sum,individualQMark)


    MarkedQuestion = zip(*individualQMark)

    for index,question in enumerate(unfilteredquestions):
        if index != 0:
            questionsForm.append(question)
        else:
            pass

    Qmark = zip(questions,individualQMark)

    for quest in questionsForm:
        questions.append(quest.label)

    SummedQuestion = (map(mean,MarkedQuestion))

    weightedQuestion = zip(questions,SummedQuestion)

    weightedEntry = zip(entries,totalEntryMark)


    return render(request, 'app/surveyAnalysis.html',locals())



def DeleteEntry(request, slug,entry_id):
    ma = Form.objects.get(slug=slug)
    entry = FormEntry.objects.filter(form = ma)
    lis = []
    for e in entry:
        lis.append(list(FieldEntry.objects.filter(entry_id=e).values_list('value',flat=True)))

    delentry = entry[int(entry_id)-1].delete()
    return render(request,'app/surveyAnalysis.html')



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


def deleteSurvey(request,id):
    Relatedform = RelatedSurvey.objects.filter(question_id=id).delete()
    return render(request,'app/indexUser.html')


def Generate_Questions(request,id,num):
    form = RelatedSurvey.objects.get(question_id=id)
    FieldFormSet = formset_factory(form=allField,extra=int(num))

    if request.method == 'POST':
        fields = FieldFormSet(request.POST)
        if fields.is_valid():
            charity_name = Field(form = form.question,label='Which Charity is Survey Intended To', field_type= 1)
            charity_name.save()
            for field in fields:
                f = field.save(commit=False)
                f.form = form.question
                f.save()
            return render (request,'app/indexAdmin.html')
        elif len(fields) == 0:
                messages.add_message(request, messages.INFO, 'Must be at least 1 Question.')
        else:
            return render (request,'app/Gen_Q.html')
    else:
        fields = FieldFormSet()
    return render(request,'app/Gen_Q.html',{'fields':fields})


def add_survey(request):
    if request.method == 'POST':
        forms = Description(request.POST)
        category = relatedSurvey(request.POST)
        if forms.is_valid():
            q = int(request.POST.get('counter'))
            linkedForm = forms.save()
            linkedSurvey = RelatedSurvey(question=linkedForm,category=request.POST.get('category'))
            linkedSurvey.save()
            return HttpResponseRedirect(reverse('gen_q', args=(linkedForm.id,q)))
        else:
            return render (request,'app/add_survey.html')
    else:
        forms = Description()
        category = relatedSurvey()
        return render(request,'app/add_survey.html',{'forms':forms,'category':category})

def redirectAfterSubmit(request,slug):
    return redirect('/')

@login_required
def send_message(request):
    user = request.user
    if request.method == 'POST':
        form = Messages(request.POST)
        if form.is_valid():
            message = form.save()
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
        form = Messages()
        if not user.is_superuser:
            return render(request,'app/send_message.html',{'form':form})
        else:
            return render(request,'app/send_messageAdmin.html',{'form':form})


#added by Shichao, to show the instruction page
def instructionAudience(request):
    return render(request, 'app/instructionAudience.html')

def instructionUser(request):
    return render(request, 'app/instructionUser.html')

def instructionAdmin(request):
    return render(request, 'app/instructionAdmin.html')
