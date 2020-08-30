from django.core.management.base import BaseCommand, CommandError
import psutil, time
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
import os

from overseer.models import VagrantBox, VagrantPoolLog
from overseer.functions.search_provider import addMoreToQueue
from overseer.functions.vagrant_controller import VagrantRunObject


import logging
logger = logging.getLogger("overseer")


class Command(BaseCommand):
    help = 'Run The Greenhouse'

    def handle(self, *args, **options):
        MAX_POOL = settings.MAX_POOL
        MEMORY_FREELIMIT = settings.MEMORY_FREELIMIT
        RUN_MINUTES = settings.RUN_MINUTES
        SLEEP_SECONDS = settings.SLEEP_SECONDS

        logger.debug("Starting Greenhouse")
        while True:
            # kill vagrants running longer than runlimit - only same worker name
            for vagBox_obj_tmp in VagrantBox.objects.filter(Q(status_code="R")|Q(status_code="I"),
                                                            processed_at__lte=(timezone.now() - timedelta(minutes=RUN_MINUTES)),
                                                            worker_name = os.uname()[1]):
                vagRunObj_tmp = VagrantRunObject(vagBox_obj_tmp.username, vagBox_obj_tmp.boxname)
                VagrantPoolLog.objects.create(status_code="D", vagrant_box=vagBox_obj_tmp, worker_name=os.uname()[1])

                logger.debug("About to destroy {}/{}".format(vagBox_obj_tmp.username, vagBox_obj_tmp.boxname))
                vagRunObj_tmp.destroy()
                logger.info("Destroyed {}/{}".format(vagBox_obj_tmp.username, vagBox_obj_tmp.boxname))
                vagBox_obj_tmp.status_code = "D"
                vagBox_obj_tmp.worker_name = os.uname()[1]
                vagBox_obj_tmp.save()


            # todo: update statuses comparing to vagrant status-global
            #  check is all running machines are running, if not mark as failed



            while VagrantBox.objects.filter(Q(status_code='W') | Q(status_code='R')| Q(status_code='I')).count() < MAX_POOL:
                vagBox_obj = VagrantBox.objects.filter(processed_at__isnull=True).exclude(status_code="W").first()
                if not vagBox_obj:
                    logger.info("No Candidates to run, requesting new results")
                    addMoreToQueue()
                    vagBox_obj = VagrantBox.objects.filter(processed_at__isnull=True).first()

                VagrantPoolLog.objects.create(status_code="W", vagrant_box=vagBox_obj, worker_name=os.uname()[1])
                logger.debug("VagrantBox {}/{} changed to 'Waiting'".format(vagBox_obj.username, vagBox_obj.boxname))
                vagBox_obj.status_code = "W"
                vagBox_obj.worker_name = os.uname()[1]
                vagBox_obj.save()
                del vagBox_obj
                #  while enough free ram, init waiting statusses and change status, update log
                #  else


            while psutil.virtual_memory().available > MEMORY_FREELIMIT and VagrantBox.objects.filter(status_code='W'):

                vagBox_obj = VagrantBox.objects.filter(status_code="W").order_by('?').first()
                vagBox_obj.status_code = "I"
                vagBox_obj.worker_name = os.uname()[1]
                vagBox_obj.save()
                logger.info("Vagrantbox starting init sequence: {}/{}, found {} candidates".format(vagBox_obj.username, vagBox_obj.boxname,
                                               VagrantBox.objects.filter(status_code="W").count() ))
                vagRunObj = VagrantRunObject(vagBox_obj.username, vagBox_obj.boxname)
                vagrantPoolLog_obj = VagrantPoolLog.objects.create(status_code="R", vagrant_box=vagBox_obj, worker_name=os.uname()[1])
                vagrantPoolLog_obj.save()

                vagRunObj.init_vagrant()
                if vagRunObj.up_vagrant():
                    vagBox_obj.processed_at = timezone.now()
                    vagBox_obj.status_code = "R"
                    logger.info("Vagrantbox initiated: {}/{}".format(vagBox_obj.username, vagBox_obj.boxname))
                    vagrantPoolLog_obj.status_message = vagRunObj.get_logs()
                else:
                    vagBox_obj.status_code = "F"
                    vagBox_obj.processed_at = timezone.now()
                    logger.error("Vagrantbox init Failed: {}/{}".format(vagBox_obj.username, vagBox_obj.boxname))
                    vagrantPoolLog_obj.status_message = vagRunObj.get_logs()
                    vagBox_obj.status_message = vagRunObj.get_logs()
                    vagRunObj.destroy()
                    logger.info("Destroyed after fail {}/{}".format(vagBox_obj.username, vagBox_obj.boxname))

                vagrantPoolLog_obj.save()

                vagBox_obj.save()
                del vagBox_obj
                del vagRunObj
                del vagrantPoolLog_obj

            if not psutil.virtual_memory().available > MEMORY_FREELIMIT and VagrantBox.objects.filter(status_code='W'):
                logger.warning("Not enough memory ({}MB) to run another Boxes, going to sleep before loop".format(
                        psutil.virtual_memory().available // 1024 // 1024))


            logger.debug("Sleep time: {}s bofore loop".format(SLEEP_SECONDS))
            time.sleep(SLEEP_SECONDS)