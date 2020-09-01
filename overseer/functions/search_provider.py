from django.conf import settings
import requests
import os, time, sys
from django.db.models import Q


from overseer.models import SearchBacklog, VagrantBox

import logging
logger = logging.getLogger("overseer")


def addMoreToQueue():

    foundOne = False
    q_keyword = 'ubuntu'

    while not foundOne:
        if SearchBacklog.objects.count():
            last_pagenumber = SearchBacklog.objects.filter(keyword=q_keyword).filter(Q(status_code="D")|Q(status_code="F")).latest('id').pagenumber
        else:
            last_pagenumber = 0


        URL = settings.VAGRANTAPI_URL + "search"
        PARAMS = {  'q': q_keyword,
                    'sort': 'created',  # downloads / created / updated
                    'order': "desc",  # desc / asc"
                    'provider': 'virtualbox',
                    'limit': 20,
                    'page': last_pagenumber+1}

        r = requests.get(url=URL, params=PARAMS, headers={"Authorization": "Bearer {}".format(settings.VAGRANTAPI_KEY)})
        if 'boxes' in r.json():
            data = r.json()['boxes']
            SearchBacklog.objects.create(pagenumber=last_pagenumber + 1, worker_name=os.uname()[1], status_code="D", keyword=q_keyword)
            for boxdetail in data:
                username, boxname = boxdetail['tag'].split("/")
                if not VagrantBox.objects.filter(username=username, boxname=boxname).count():
                    vag_obj = VagrantBox.objects.create(username=username, boxname=boxname, description=boxdetail,
                                                        worker_name=os.uname()[1])
                    vag_obj.tags.add('autoadded', )
                    logger.debug("Box ADDED: {}".format(boxdetail['tag']))
                    foundOne = True
                else:
                    logger.debug("Box skipped: {}".format(boxdetail['tag']))

            time.sleep(1)

        else:
            SearchBacklog.objects.create(pagenumber=last_pagenumber + 1, worker_name=os.uname()[1], status_code="W", keyword=q_keyword,
                                         status_message=r.json())
            logger.warning("Search API failure. Request{}, Paramaters:{}, Response: {}".format(URL, PARAMS, r.json()))

            # softfail - same page failed 3 times (W)-  change status to failed
            if SearchBacklog.objects.filter(pagenumber=last_pagenumber + 1, status_code="W",keyword=q_keyword).count()>2:
                logger.warning(
                    "Search API failed for same pagenumber >2 times! marked as failed page and moving on. Request{}, Paramaters:{}, Response: {}".format(URL, PARAMS, r.json()))
                SearchBacklog.objects.create(pagenumber=last_pagenumber + 1, worker_name=os.uname()[1], status_code="F",
                                             keyword=q_keyword, status_message=r.json())

            #  todo: if hardfail - 3 pages in row failed - exit
            if SearchBacklog.objects.filter( status_code="F", keyword=q_keyword)\
                    .filter(Q(pagenumber=last_pagenumber + 1) | Q(last_pagenumber) | Q(last_pagenumber + 1)).count() > 2:
                logger.error(
                    "Search API failed for >2 pages in row! Hard Exit. Request{}, Paramaters:{}, Response: {}".format(
                        URL, PARAMS, r.json()))
                SearchBacklog.objects.create(pagenumber=last_pagenumber + 1, worker_name=os.uname()[1],
                                             status_code="F",
                                             keyword=q_keyword, status_message=r.json())
                sys.exit(1)
            time.sleep(20) #  Failed api call timer




