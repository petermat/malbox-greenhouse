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
                                                            worker_name=os.uname()[1]):
                vagRunObj_tmp = VagrantRunObject(vagBox_obj_tmp.username, vagBox_obj_tmp.boxname)
                VagrantPoolLog.objects.create(status_code="D", vagrant_box=vagBox_obj_tmp, worker_name = os.uname()[1])

                logger.debug("About to destroy {}/{}. Served for {} minutes.".format(vagBox_obj_tmp.username, vagBox_obj_tmp.boxname,SLEEP_SECONDS))
                vagRunObj_tmp.destroy()
                logger.info("Destroyed {}/{}, natural cause".format(vagBox_obj_tmp.username, vagBox_obj_tmp.boxname))
                vagBox_obj_tmp.status_code = "D"
                vagBox_obj_tmp.worker_name = os.uname()[1]
                vagBox_obj_tmp.save()


            # todo: update statuses comparing to vagrant status-global
            #  check is all running machines are running, if not mark as failed
            #   1. compare running machines to box.status = ['f','d'], if match destroy manually
            from overseer.functions.vagrant_controller import getActiveVagrantboxes
            allboxes_dict = getActiveVagrantboxes()
            if allboxes_dict:
                running_machines = [x.split("/") for x, y in allboxes_dict.items() if y == 'running']

                for username, boxname in running_machines:
                    # todo: ifstatus in DB is D or F, kill machine
                    if VagrantBox.objects.filter(username=username, boxname=boxname).filter(Q(status_code="F")|Q(status_code="D")).count():
                        VagrantRunObject(username=username, boxname=boxname).destroy()
                        logger.warning("VagrantBox {}/{} was found to be running in global status but NOT in DB. Destroying.".format(username, boxname))

                # todo: 2. compare running machines to box.status = ['r','i'], if not match mark as failed and destroy manually
                #  list all boxes with status 'r' or 'i' and if machines is not listed as running in global, mark manually
                for vagBox_tmp1 in VagrantBox.objects.filter(Q(status_code="R")|Q(status_code="I")).filter(worker_name = os.uname()[1]):
                    if [vagBox_tmp1.username, vagBox_tmp1.boxname] not in running_machines:
                        logger.warning("VagrantBox {}/{} was found NOT to be running in global status but is DB. Marking as failed.".format(vagBox_tmp1.username, vagBox_tmp1.boxname))
                        vagBox_tmp1.status_code = "F"
                        vagBox_tmp1.status_message = "VagrantBox {}/{} was found NOT to be running in global status but is DB. Marking as failed.".format(vagBox_tmp1.username, vagBox_tmp1.boxname)
                        vagBox_tmp1.save()
                        VagrantPoolLog.objects.create(status_code="F", vagrant_box=vagBox_obj, worker_name=os.uname()[1],
                                                      status_message="found NOT to be running in global status but is DB. Marking as failed")

            while VagrantBox.objects.filter(Q(status_code='W') | Q(status_code='R')| Q(status_code='I')).count() < MAX_POOL:
                vagBox_obj = VagrantBox.objects.filter(processed_at__isnull=True).exclude(status_code="W").first()
                if not vagBox_obj:
                    logger.info("No Candidates to run, requesting new results")
                    addMoreToQueue()
                    vagBox_obj = VagrantBox.objects.filter(processed_at__isnull=True).first()

                VagrantPoolLog.objects.create(status_code="W", vagrant_box=vagBox_obj, worker_name = os.uname()[1])
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
                vagrantPoolLog_obj = VagrantPoolLog.objects.create(status_code="I", vagrant_box=vagBox_obj, worker_name = os.uname()[1])
                vagrantPoolLog_obj.save()

                vagRunObj.init_vagrant()
                if vagRunObj.up_vagrant():
                    vagBox_obj.processed_at = timezone.now()
                    vagBox_obj.status_code = "R"
                    vagBox_obj.status_message = vagRunObj.get_logs()
                    logger.info("Vagrantbox initiated: {}/{}".format(vagBox_obj.username, vagBox_obj.boxname))
                    vagrantPoolLog_obj = VagrantPoolLog.objects.create(status_code="R", vagrant_box=vagBox_obj,
                                                                       worker_name=os.uname()[1])
                    vagrantPoolLog_obj.status_message = vagRunObj.get_logs()
                    vagrantPoolLog_obj.save()
                else:
                    vagBox_obj.status_code = "F"
                    vagBox_obj.processed_at = timezone.now()
                    logger.error("Vagrantbox init Failed: {}/{}".format(vagBox_obj.username, vagBox_obj.boxname))
                    vagrantPoolLog_obj = VagrantPoolLog.objects.create(status_code="F", vagrant_box=vagBox_obj,
                                                                       worker_name=os.uname()[1])
                    vagrantPoolLog_obj.status_message = vagRunObj.get_logs()
                    vagrantPoolLog_obj.save()
                    vagBox_obj.status_message = vagRunObj.get_logs()
                    vagRunObj.destroy()
                    logger.info("Destroyed after fail {}/{}".format(vagBox_obj.username, vagBox_obj.boxname))

                vagBox_obj.save()
                #del vagBox_obj
                #del vagRunObj
                #del vagrantPoolLog_obj

            if VagrantBox.objects.filter(status_code='W') and not psutil.virtual_memory().available > MEMORY_FREELIMIT:
                logger.warning("Not enough memory ({}MB) to run another Boxes, going to sleep before loop".format(
                        psutil.virtual_memory().available // 1024 // 1024))


            logger.debug("Sleep time: {}s bofore loop".format(SLEEP_SECONDS))
            time.sleep(SLEEP_SECONDS)