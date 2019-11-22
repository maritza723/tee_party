from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^validate_login$', views.validate_login),
    url(r'^dashboard$', views.dashboard),
    url(r'^edit/(?P<golfer_id>\d+)$', views.edit),
    url(r'^update/(?P<golfer_id>\d+)$', views.update),
    url(r'^new_course$', views.new),
    url(r'^create$', views.create),
    url(r'^all_courses$', views.allCourses),
    url(r'^course/(?P<course_id>\d+)$', views.course),
    url(r'^schedule/(?P<course_id>\d+)$', views.schedule),
    url(r'^teeTime/(?P<course_id>\d+)$', views.teeTime),
    url(r'^delete/(?P<teeTime_id>\d+)$', views.delete),
]