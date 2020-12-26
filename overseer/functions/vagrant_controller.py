from django.conf import settings
import os
import shutil

import time
import timeout_decorator

import vagrant

import subprocess
import logging
logger = logging.getLogger("overseer")



def getActiveVagrantboxes():

    # vagrant global-status --prune
    # vagrant global-Vagrant about to UPstatus --machine-readable

    subprocess.run(['vagrant', 'global-status', '--prune'], stdout=subprocess.PIPE)
    result = subprocess.run(['vagrant', 'global-status', '--machine-readable'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')

    parsed_lines = [line.split(',', 4) for line in output.splitlines() if line.strip()]
    #parsed_lines = list(filter(lambda x: x[2] not in ["metadata", "ui", "action"], parsed_lines))
    parsed_lines = list(filter(lambda x: x[2] in ["machine-home", "state"], parsed_lines))
    parsed_lines_dict = dict()
    if parsed_lines:
        for counter, line in enumerate(parsed_lines):
            if counter % 2 == 1:
                parsed_lines_dict["/".join(parsed_lines[counter-1][-1].split('/')[-2:])] = line[-1]
    return parsed_lines_dict




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
        logger.debug("Vagrantfile native object created: {}/{}".format(username, boxname),
                     extra={'box': '{}/{}'.format(self.username, self.boxname)}
                     )


    def init_vagrant(self):
        #def prepare_vagrantfile(self, username, boxname):
        from django.template.loader import render_to_string

        templatefile = os.path.join(settings.VAGRANT_TEMPLATEFOLDER, 'Vagrantfile' )
        context = {'username': self.username,
                   'boxname': self.boxname,
                   'username_no_underscore': self.username.replace("_", "-"),  # hostname cannot contain underscore !!!
                   'boxname_no_underscore': self.boxname.replace("_", "-")}  # hostname cannot contain underscore !!!


        shutil.rmtree(self.vagrantdir_path, ignore_errors=True)
        #Path(self.vagrantdir_path).mkdir(parents=True, exist_ok=True)
        shutil.copytree(settings.VAGRANT_TEMPLATEFOLDER, self.vagrantdir_path)
        logger.debug("Blueprint files copied to Vagrantile folder {}/{}".format(self.username, self.boxname))

        open(os.path.join(self.vagrantdir_path, 'Vagrantfile'), "w").write(render_to_string(templatefile, context))
        logger.debug("Vagrantfile prepared: {}/{}".format(self.username, self.boxname),
                     extra={'box': '{}/{}'.format(self.username, self.boxname)}
                     )

    @timeout_decorator.timeout(60*60)
    def up_vagrant(self):
        logger.debug("Vagrant about to UP: {}".format(self.vagrantdir_path),
                     extra={'box': '{}/{}'.format(self.username, self.boxname)})
        try:
            #self.native_obj.up()

            # todo: try up(stream_output=True), printing by lane to debug
            # output-> generator yielding lines of output
            for outline in self.native_obj.up(stream_output=True):
                print("\033[37m  "+outline.strip()+"\033[0m")
            logger.info("Vagrant Box UP done: {}".format(self.vagrantdir_path),
                        extra={'box': '{}/{}'.format(self.username, self.boxname)})
            return True
        except Exception as Err:
            logger.error("Vagrant init filed: {}".format(Err),
                         extra={'box': '{}/{}'.format(self.username, self.boxname)})
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
            logger.warning("Vagrant destroy failed! {}/{}".format(self.username, self.boxname),
                           extra={'box': '{}/{}'.format(self.username, self.boxname)})
        os.system("cd {} && vagrant destroy --force".format(self.vagrantdir_path))
        shutil.rmtree(os.path.join(os.environ['HOME'], '.vagrant.d', 'boxes', '{}-VAGRANTSLASH-{}'.format(self.username, self.boxname)),
                      ignore_errors=True
                      )
        logger.info("Box destroyed: {}/{}".format(self.username, self.boxname),
                    extra={'box': '{}/{}'.format(self.username, self.boxname)}
                    )

    def status(self):
        self.native_obj.status()



