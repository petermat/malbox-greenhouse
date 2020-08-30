

## Install

sudo apt install python3-virtualenv
vagrant plugin install vagrant-vbguest


Manual actions:

- Activate http listener in Splunk and add token to settings_local
- Add port 9997 to splunk inputs

- Download splunkforwarder binary to blueprint/xxx/splunkforwarder/
  - wget -O splunkforwarder-8.0.5-a1a6394cc5ae-Linux-x86_64.tgz 'https://www.splunk.com/bin/splunk/DownloadActivityServlet?architecture=x86_64&platform=linux&version=8.0.5&product=universalforwarder&filename=splunkforwarder-8.0.5-a1a6394cc5ae-Linux-x86_64.tgz&wget=true'


- limit access to internal private_network (https://www.frozentux.net/iptables-tutorial/chunkyhtml/x2702.html#TABLE.IPRANGEMATCH)
  `iptables -A OUTPUT -m iprange --dst-range 192.168.4.0-192.168.4.255 -j DROP`
  `iptables -A OUTPUT -m iprange --dst-range 192.168.38.1-192.168.38.198 -j DROP`

-extend partition
- `sudo lvextend -l +47616 /dev/vgvagrant/root`
- `sudo resize2fs -p /dev/vgvagrant/root`

## Init App

- `python manage.py migrate --run-syncdb`
- `python manage.py createsuperuser`
- `vagrant plugin install vagrant-disksize`
- `vagrant plugin install vagrant-vbguest`


Run Greenhouse

- `python manage.py run_greenhouse`



## Tests

Add to pool

`from overseer.functions.search_provider import addMoreToQueue`

`addMoreToQueue()`


Start Loop

`from overseer.functions.search_provider import VagrantLoop`

`VagrantLoop().start()`
