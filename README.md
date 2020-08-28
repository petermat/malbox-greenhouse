

## Install

sudo apt install python3-virtualenv
vagrant plugin install vagrant-vbguest


Manual actions:

- Activate http listener in Splunk and add token to settings_local

## Test

Add to pool

`from overseer.functions.search_provider import addMoreToQueue`

`addMoreToQueue()`


Start Loop

`from overseer.functions.search_provider import VagrantLoop`

`VagrantLoop().start()`



