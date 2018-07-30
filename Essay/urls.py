from django.conf.urls import url
from .models import Essay
from . import views

urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/edit$', views.EssayUpdate.as_view(), name="essay_update"),
    url(r'^(?P<slug>[-\w]+)/$', views.EssayDetail.as_view(), name="essay_detail"),
    url(r'^all/(?P<category>[\w]+)/$', views.EssayList.as_view(), name="essay_list"),
    #url(r'^all/meditations/$', views.EssayList.as_view(), name="all_meditations"),
]

