# Project Malbox-Greenhouse

Deploy Vagrant boxes in controlled environment, observe then, and identify deviations.

## Install

### Deploy Splunk & PostgreSQL

`vagrant up malbox-logger`

- Activate http listener in Splunk and add token to settings_local

- Add port 9997 to splunk inputs

- add database and credentials matching `project_greenhouse/settings_local.py`


### Deploy Workers

Create and fill local settings

  `nano project_greenhouse/settings_local.py`


Download splunkforwarder binary to overseer/blueprints/ubuntu1/splunkforwarder/

  `wget -O splunkforwarder-8.0.5-a1a6394cc5ae-Linux-x86_64.tgz 'https://www.splunk.com/bin/splunk/DownloadActivityServlet?architecture=x86_64&platform=linux&version=8.0.5&product=universalforwarder&filename=splunkforwarder-8.0.5-a1a6394cc5ae-Linux-x86_64.tgz&wget=true'`


Limit access to different network (https://www.frozentux.net/iptables-tutorial/chunkyhtml/x2702.html#TABLE.IPRANGEMATCH)
  
  `iptables -A OUTPUT -m iprange --dst-range 192.168.4.0-192.168.4.255 -j DROP`
  

Extend partition

  - extend manually in gparted and extend:
  - `sudo lvextend -l +47616 /dev/vgvagrant/root`
  - `sudo resize2fs -p /dev/vgvagrant/root`


Install Vagrant Plugins

  - `vagrant plugin install vagrant-disksize`
  - `vagrant plugin install vagrant-vbguest`


## Init App

If database wasnt initiated yet, run:

  - `python manage.py migrate --run-syncdb`
  - `python manage.py createsuperuser`

Activate venv and install requirements

- `source venv/bin/activate`
- `pip install -r requirements.txt`

Run Greenhouse

- `python manage.py run_greenhouse`

Run Webserver

- `python manage.py runserver`


## Tests

Add to pool

`from overseer.functions.search_provider import addMoreToQueue`

`addMoreToQueue()`


Start Loop

`from overseer.functions.search_provider import VagrantLoop`

`VagrantLoop().start()`
