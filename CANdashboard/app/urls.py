from django.conf.urls import url, include
from app import views
from django.contrib import admin

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^.*\.html', views.gentella_html, name='gentella'),

    # The home page
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'(?P<Name>[-\w]+)/$',views.Charity_detail, name = 'charity_detail'),
]
