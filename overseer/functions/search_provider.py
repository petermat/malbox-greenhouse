from django.conf import settings
import requests

from overseer.models import SearchBacklog, VagrantBox

import logging
logger = logging.getLogger("overseer")


def addMoreToQueue():

    foundOne = False
    while not foundOne:
        if SearchBacklog.objects.count():
            last_pagenumber = SearchBacklog.objects.latest('id').pagenumber
        else:
            last_pagenumber = 0

        URL = settings.VAGRANTAPI_URL + "search"
        PARAMS = {  'q': 'ubuntu',
                    'sort': 'created',  # downloads / created / updated
                    'order': "desc",  # desc / asc"
                    'provider': 'virtualbox',
                    'limit': 20,
                    'page': last_pagenumber+1}

        r = requests.get(url=URL, params=PARAMS, headers={"Authorization": "Bearer {}".format(settings.VAGRANTAPI_KEY)})
        data = r.json()['boxes']


        if not data:
            logger.warning("Search result empty! Exit")
            break

        for boxdetail in data:
            username, boxname = boxdetail['tag'].split("/")
            if not VagrantBox.objects.filter(username=username, boxname=boxname).count():
                vag_obj = VagrantBox.objects.create(username=username, boxname=boxname, description=boxdetail)
                vag_obj.tags.add('autoadded')
                logger.debug("Box ADDED: {}".format(boxdetail['tag']))
                foundOne = True
            else:
                logger.debug("Box skipped: {}".format(boxdetail['tag']))

        SearchBacklog.objects.create(pagenumber=last_pagenumber+1)
