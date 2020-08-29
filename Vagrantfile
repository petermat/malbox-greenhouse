# require vagrant plugin install vagrant-disksize

Vagrant.configure("2") do |config|
    config.vm.define "malbox-greenhouse" do |cfg|
        cfg.ssh.username = "vagrant"
        cfg.ssh.password = "vagrant"
        cfg.vm.box = "bento/ubuntu-20.04"
        cfg.vm.hostname = "malbox-greenhouse"
        cfg.disksize.size = '450GB'
        #config.vbguest.auto_update = true # virtualbox tools
        cfg.vm.synced_folder ".", "/vagrant"
        cfg.vm.network :private_network, ip: "192.168.38.162", gateway: "192.168.38.1", dns: "8.8.8.8"
        cfg.vm.provision :shell, path: "vagrant/1system.sh"
        cfg.vm.provision :reload #"reload"
        #cfg.vm.provision :shell, path: "2bootstrap.sh"
        cfg.vm.provision "file", source: "vagrant/id_rsa", destination: "/home/vagrant/.ssh/id_rsa"
        cfg.vm.provision "file", source: "vagrant/id_rsa.pub", destination: "/home/vagrant/.ssh/id_rsa.pub"
        #cfg.vm.provision "file", source: "resources/000-default.conf", destination: "/home/vagrant/000-default.conf"
        cfg.vm.provision "shell", inline: "chmod 600 /home/vagrant/.ssh/id_rsa"
        #cfg.vm.provision "shell", inline: "mkdir /home/vagrant/workspace && cp -RT /vagrant /home/vagrant/workspace"
	cfg.vm.provision :shell, path: "vagrant/3app.sh", privileged: false

        cfg.vm.provider "virtualbox" do |vb, override|
            vb.gui = true
            vb.name = "malbox-greenhouse"
            vb.customize ["modifyvm", :id, "--memory", 38912 ] # 30 + 8 * 1024
            vb.customize ["modifyvm", :id, "--cpus", 16]
            vb.customize ["modifyvm", :id, "--vram", "128"]
            vb.customize ["modifyvm", :id, "--graphicscontroller", "vmsvga"]
            vb.customize ["modifyvm", :id, "--nested-hw-virt", "on"]
            vb.customize ["modifyvm", :id, "--nicpromisc2", "allow-all"]
            vb.customize ["modifyvm", :id, "--clipboard-mode", "bidirectional"]
            vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
            vb.customize ["setextradata", "global", "GUI/SuppressMessages", "all" ]
            #vb.customize ["modifyvm", :id, "--cpuexecutioncap", "50"]
        end

    end

 config.vm.define "malbox-logger" do |cfg|
    cfg.vm.box = "bento/ubuntu-18.04"
    cfg.vm.hostname = "malbox-logger"
    cfg.vm.provision :shell, path: "logger.sh"
    cfg.vm.network :private_network, ip: "192.168.38.199", gateway: "192.168.38.1", dns: "8.8.8.8"

    cfg.vm.provider "virtualbox" do |vb, override|
      vb.gui = true
      vb.name = "malbox-logger"
      vb.customize ["modifyvm", :id, "--memory", 4096]
      vb.customize ["modifyvm", :id, "--cpus", 2]
      vb.customize ["modifyvm", :id, "--vram", "32"]
      vb.customize ["modifyvm", :id, "--nicpromisc2", "allow-all"]
      vb.customize ["modifyvm", :id, "--clipboard", "bidirectional"]
      vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      vb.customize ["setextradata", "global", "GUI/SuppressMessages", "all" ]
    end
  end

end
