from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<part_id>[0-9]+)/$', views.indented, name='indented'),
    url(r'^(?P<part_id>[0-9]+)/export/$', views.export_part_indented, name='export-part-indented'),
    url(r'^(?P<part_id>[0-9]+)/upload/$', views.upload_part_indented, name='upload-part-indented'),
    url(r'^(?P<part_id>[0-9]+)/part_match/$', views.octopart_part_match, name='octopart-part-match'),
    url(r'^export/$', views.export_part_list, name='export-part-list'),
]