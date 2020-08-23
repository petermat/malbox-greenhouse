from django.conf import settings
import os, time
import shutil
from django.utils import timezone

from overseer.models import VagrantBox
from overseer.functions.search_provider import addMoreToQueue
import vagrant
import psutil

import logging
logger = logging.getLogger("overseer")

class VagrantRunObject:
    def __init__(self):
        self.native_obj = None
        self.vagrantfile_path = None

    def prepare_vagrantfile(self, username, boxname):
        from django.template.loader import render_to_string
        template = settings.VAGRANT_TEMPLATEFILE
        context = {'username': username, 'boxname': boxname}

        from pathlib import Path
        self.vagrantdir_path = os.path.join(settings.TMPSPACE, username, boxname)
        Path(self.vagrantdir_path).mkdir(parents=True, exist_ok=True)

        open(os.path.join(self.vagrantdir_path, 'Vagrantfile'), "w").write(render_to_string(template, context))
        logger.debug("Vagrantfile prepared: {}/{}".format(username, boxname))


    def init_vagrant(self):
        env = os.environ.copy()
        env['PWD'] = self.vagrantdir_path

        #v.env = os_env
        self.native_obj = vagrant.Vagrant(self.vagrantdir_path, quiet_stdout=False, quiet_stderr=False, env=env)
        self.native_obj.up()
        logger.debug("Vagrant Box UP: {}".format(self.vagrantdir_path))


    def destroy(self, username, boxname):
        self.native_obj.destroy()
        shutil.rmtree(os.path.join(os.environ['HOME'], '.vagrant.d', 'boxes', '{}-VAGRANTSLASH-{}'.format(username, boxname)))
        logger.info("Box destroyed: {}/{}".format(username, boxname))

    def status(self):
        self.native_obj.status(name='default')



class VagrantLoop:
    def __init__(self):
        pass

    def start(self):
        while True:
            if psutil.virtual_memory().available // 1024 // 1024 > 1024:
                if VagrantBox.objects.filter(processed_at__isnull=True):
                    vag_obj = VagrantBox.objects.filter(processed_at__isnull=True).latest('id')
                    logger.debug("Vagrantbox about to init: {}/{}, found {} candidates".format(vag_obj.username, vag_obj.boxname,
                                                   VagrantBox.objects.filter(processed_at__isnull=True).count() ))
                    obj = VagrantRunObject()
                    obj.prepare_vagrantfile(vag_obj.username, vag_obj.boxname)
                    obj.init_vagrant()
                    logger.debug("Vagrantbox initiated: {}/{}".format(vag_obj.username, vag_obj.boxname))
                    time.sleep(10)
                    logger.debug("About to destroy {}/{}".format(vag_obj.username, vag_obj.boxname))
                    obj.destroy(vag_obj.username, vag_obj.boxname)
                    logger.debug("Destroyed {}/{}".format(vag_obj.username, vag_obj.boxname))
                    vag_obj.processed_at = timezone.now()
                    vag_obj.save()
                else:
                    logger.info("No Candidates to run, requesting new results")
                    addMoreToQueue()
            else:
                logger.warning("Not enough memory to run: {}".format(psutil.virtual_memory().available // 1024 // 1024))
                break
