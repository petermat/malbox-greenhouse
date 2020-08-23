from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.homePageView, name='index'),
    path('apiresults/', views.searchCloudView, name='apiresults'),
    path('vagresults/', views.vagrantObjectsView, name='vagresults'),
    path('apiBoxDetail/', views.apiBoxDetailView, name='apiBoxDetail'),
    #path('archive/', views.blog.archive),
]