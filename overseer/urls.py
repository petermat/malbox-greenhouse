from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.homePageView),
    #path('archive/', views.blog.archive),
]