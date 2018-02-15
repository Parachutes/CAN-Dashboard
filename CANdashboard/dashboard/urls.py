from django.conf.urls import url, include
from dashboard import views
from django.contrib import admin

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^.*\.html', views.gentella_html, name='gentella'),

    url(r'^admin/', include(admin.site.urls)),

    # pages for audiences/ users/ administrators
    url(r'^$', views.index, name='index'),
    url(r'^myUser/', views.indexUser, name='indexUser'),
    url(r'^myAdmin/', views.indexAdmin, name='indexAdmin'),

    # to be deleted just for testing
    url(r'^test/', views.indexTest, name='indexTest'),

    url(r'(?P<Name>[-\w]+)/$',views.Charity_detail, name = 'charity_detail'),



]
