from django.conf.urls import url, include
from dashboard import views
from django.contrib import admin
from django.contrib import admin
import forms_builder.forms.urls
from directmessages.apps import Inbox
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.

    url(r'^admin/', include(admin.site.urls)),
    url('accounts/', include('django.contrib.auth.urls')),
    #url(r'^logout/$', 'django.contrib.auth.views.logout',
                          #{'next_page': '/'}),

    url(r'^forms/', include(forms_builder.forms.urls)),
    url(r'^profile/$', views.indexUser, name='indexUser'),
    url(r'^messages/$',views.list_messages,name='messages'),
    url(r'^survey_list/$',views.list_survey,name='survey_list'),
    url(r'^charity_list/$',views.list_charity,name='charity_list'),
    url(r'^add/$',views.add_survey,name='messages'),
    url(r'^register/$',views.register_page,name='register'),
    # pages for audiences/ users/ administrators
    url(r'^$', views.index, name='index'),
    url(r'^myUser/', views.indexUser, name='indexUser'),
    #url(r'^myAdmin/', views.indexAdmin, name='indexAdmin'),

    # to be deleted just for testing
    #url(r'^test/', views.indexTest, name='indexTest'),

    url(r'(?P<Name>[-\w]+)/$',views.Charity_detail, name = 'charity_detail'),



]
