
install_osquery(){
  echo "deb [arch=amd64] https://pkg.osquery.io/deb deb main" | sudo tee /etc/apt/sources.list.d/osquery.list
  sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 1484120AC4E9F8A1A577AEEE97A80C63C9D8B80B
  apt-get update
  apt-get install -y osquery
  cp -RT /vagrant/osquery /etc/osquery
  systemctl enable osqueryd
  systemctl start osqueryd
}

install_splunkforwarder(){

  UF_SERVER_ADDRESS="192.168.38.199"
  UF_SERVER_PORT=9997

  #!/bin/bash
  mkdir /opt/splunkforwarder
  #cp /vagrant/splunkf/splunkforwarder-8.0.5-a1a6394cc5ae-Linux-x86_64.tgz /opt/splunkforwarder
  tar xvfz /vagrant/splunkforwarder/splunkforwarder-8.0.5-a1a6394cc5ae-Linux-x86_64.tgz -C /opt
  cp /vagrant/splunkforwarder/user-seed.conf /opt/splunkforwarder/etc/system/local/user-seed.conf

  /opt/splunkforwarder/bin/splunk start --accept-license --answer-yes --auto-ports --no-prompt
  /opt/splunkforwarder/bin/splunk enable boot-start #-user splunk --accept-license
  /opt/splunkforwarder/bin/splunk add forward-server ${UF_SERVER_ADDRESS}:${UF_SERVER_PORT} -auth admin:changeme
  /opt/splunkforwarder/bin/splunk add monitor "/var/log/osquery/osqueryd.results.log" -index main -sourcetype "osquery:results"

  #/opt/splunkforwarder/bin/splunk add monitor "/var/log/osquery/osqueryd.*INFO*" -index main -sourcetype "osquery:info"
  #/opt/splunkforwarder/bin/splunk add monitor "/var/log/osquery/osqueryd.*ERROR*" -index main -sourcetype "osquery:error"
  #/opt/splunkforwarder/bin/splunk add monitor "/var/log/osquery/osqueryd.*WARNING*" -index main -sourcetype "osquery:warning"
}




main(){
  install_osquery
  install_splunkforwarder
}


main
exit 0
