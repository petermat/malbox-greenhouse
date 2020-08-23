from django.shortcuts import render
import requests

from django.conf import settings

from .tables import *

def homePageView(request):
    context = {}
    from .functions.vagrant_controller import VagrantRunObject
    obj = VagrantRunObject()
    return render(request, 'index.html', context)


def vagrantObjectsView(request):
    data = VagrantBox.objects.all()
    table = VagrantBoxTable(data)
    context = {'table': table}
    return render(request, 'searchresults.html', context)




def searchCloudView(request):

    # vagrant api search https://www.vagrantup.com/vagrant-cloud/api.html#search
    URL = settings.VAGRANTAPI_URL + "search"
    PARAMS = {  'q': 'ubuntu',
                'sort': 'created',  # downloads / created / updated
                'order': "desc",  # desc / asc"
                'provider': 'virtualbox',
                'limit': 20,
                'page': 1}

    r = requests.get(url=URL, params=PARAMS, headers={"Authorization": "Bearer {}".format(settings.VAGRANTAPI_KEY)})
    data = r.json()['boxes']
    table = SearchApiResultsTable(data)
    context = {'table': table,}
    return render(request, 'searchresults.html', context)


def apiBoxDetailView(request):
    # vagrant api search https://www.vagrantup.com/vagrant-cloud/api.html#search
    URL = settings.VAGRANTAPI_URL + "box/" + "peterm/"+"pokebox/"

    r = requests.get(url=URL, headers={"Authorization": "Bearer {}".format(settings.VAGRANTAPI_KEY)})
    data = r.json()
    from pprint import pprint
    table = SearchApiResultsTable([data,])
    context = {'table': table,}
    return render(request, 'searchresults.html', context)