from django.conf import settings
import os
import shutil



import vagrant


import logging
logger = logging.getLogger("overseer")

class VagrantRunObject:
    def __init__(self, username, boxname):
        self.username = username
        self.boxname = boxname

        from pathlib import Path
        self.vagrantdir_path = os.path.join(settings.TMPSPACE, username, boxname)

        #env = os.environ.copy()
        #env['PWD'] = self.vagrantdir_path

        #v.env = os_env

        log_cm = vagrant.make_file_cm(os.path.join(self.vagrantdir_path, 'deployment.log'))
        self.native_obj = vagrant.Vagrant(self.vagrantdir_path,
                                          out_cm=log_cm, err_cm=log_cm,
                                          quiet_stdout=False, quiet_stderr=False,
                                          #env=env
                                          )
        #logger.debug("error_obj: ", error_obj)
        logger.debug("Vagrantfile native object created: {}/{}".format(username, boxname))


    def init_vagrant(self):
        #def prepare_vagrantfile(self, username, boxname):
        from django.template.loader import render_to_string

        templatefile = os.path.join(settings.VAGRANT_TEMPLATEFOLDER, 'Vagrantfile' )
        context = {'username': self.username, 'boxname': self.boxname}


        shutil.rmtree(self.vagrantdir_path, ignore_errors=True)
        #Path(self.vagrantdir_path).mkdir(parents=True, exist_ok=True)
        shutil.copytree(settings.VAGRANT_TEMPLATEFOLDER, self.vagrantdir_path)
        logger.debug("Blueprint files copied to Vagrantile folder {}/{}".format(self.username, self.boxname))

        open(os.path.join(self.vagrantdir_path, 'Vagrantfile'), "w").write(render_to_string(templatefile, context))
        logger.debug("Vagrantfile prepared: {}/{}".format(self.username, self.boxname))


    def up_vagrant(self):
        logger.debug("Vagrant about to UP: {}".format(self.vagrantdir_path))
        try:
            self.native_obj.up()
            logger.info("Vagrant Box UP done: {}".format(self.vagrantdir_path))
            return True
        except Exception as Err:
            logger.error("Vagrant init filed: {}".format(Err))
            return False


    def get_logs(self):
        # Open a file: file
        file = open(os.path.join(self.vagrantdir_path, 'deployment.log'), mode='r')
        content = file.read()
        logger.debug("Logs retrieved, size: {}".format(len(content)))
        file.close()
        return content

    def destroy(self):
        try:
            self.native_obj.destroy()
        except Exception as Err:
            logger.warning("Vagrant destroy failed!")
        os.system("cd {} && vagrant destroy".format(self.vagrantdir_path))
        shutil.rmtree(os.path.join(os.environ['HOME'], '.vagrant.d', 'boxes', '{}-VAGRANTSLASH-{}'.format(self.username, self.boxname)),
                      ignore_errors=True
                      )
        logger.info("Box destroyed: {}/{}".format(self.username, self.boxname))

    def status(self):
        self.native_obj.status()



