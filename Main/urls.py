from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', views.register),
    path('', views.index),
    path('login/', views.login),
    path('view/', views.viewUsers),
    path('logout/', views.logout),
    path('courses/', views.courses),
    path('compreview/', views.compReview),
    path('contactus/', views.contactus),
    path('codingcomp/', views.codingcomp),
    # path('deleteall/', views.delete_all),
    path('activate/', views.activate),
    path('dashboard/', views.dashboard),
    path('accsettings/', views.accSettings),
    path('yourcourses/', views.yourCourses),
    path('yourtests/', views.yourTests),
    path('joinedcomps/', views.joinedcomps),
    path('compiler/', views.compiler),
    path('taketest/<slug:test_id>/', views.takeTest),
    path('starttest/<slug:test_id>/', views.startTest),
    path('subject/<slug:course_id>/', views.subject),
    path('subject/<slug:course_id>/joincourse', views.joinCourse),
    path('tests/', views.tests),
    path('testscores/', views.testScores),
    path('studymaterials/', views.studymaterials),
    path('feedback/', views.feedback),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)