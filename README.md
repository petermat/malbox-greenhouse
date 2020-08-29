

## Install

sudo apt install python3-virtualenv
vagrant plugin install vagrant-vbguest


Manual actions:

- Activate http listener in Splunk and add token to settings_local
- Add port 9997 to splunk inputs


Init App

-  `python manage.py migrate --run-syncdb`
-  `python manage.py createsuperuser`


Run Greenhouse

- `python manage.py run_greenhouse`



## Tests

Add to pool

`from overseer.functions.search_provider import addMoreToQueue`

`addMoreToQueue()`


Start Loop

`from overseer.functions.search_provider import VagrantLoop`

`VagrantLoop().start()`
