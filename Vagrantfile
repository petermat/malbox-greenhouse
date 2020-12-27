# require vagrant plugin install vagrant-disksize

Vagrant.configure("2") do |config|
    config.vm.define "malbox-greenhouse-worker1" do |cfg|
        cfg.ssh.username = "vagrant"
        cfg.ssh.password = "vagrant"
        cfg.vm.box = "bento/ubuntu-20.04"
        cfg.vm.hostname = "malbox-greenhouse-worker1"
        cfg.disksize.size = '250GB'
        #config.vbguest.auto_update = true # virtualbox tools
        cfg.vm.synced_folder ".", "/vagrant"
        cfg.vm.network :private_network, ip: "192.168.38.162", gateway: "192.168.38.1", dns: "8.8.8.8"
        cfg.vm.provision :shell, path: "vagrant/1system.sh"
        cfg.vm.provision :reload #"reload"
        #cfg.vm.provision :shell, path: "2bootstrap.sh"
        #cfg.vm.provision "file", source: "vagrant/id_rsa", destination: "/home/vagrant/.ssh/id_rsa"
        #cfg.vm.provision "file", source: "vagrant/id_rsa.pub", destination: "/home/vagrant/.ssh/id_rsa.pub"
        #cfg.vm.provision "file", source: "resources/000-default.conf", destination: "/home/vagrant/000-default.conf"
        #cfg.vm.provision "shell", inline: "chmod 600 /home/vagrant/.ssh/id_rsa"
        #cfg.vm.provision "shell", inline: "mkdir /home/vagrant/workspace && cp -RT /vagrant /home/vagrant/workspace"
	      cfg.vm.provision :shell, path: "vagrant/3app.sh", privileged: false

        cfg.vm.provider "virtualbox" do |vb, override|
            vb.gui = true
            vb.name = "malbox-greenhouse-worker1"
            vb.customize ["modifyvm", :id, "--memory", 8192 ] # 30 + 8 * 1024
            vb.customize ["modifyvm", :id, "--cpus", 6]
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

    config.vm.define "malbox-greenhouse-worker2" do |cfg|
        cfg.ssh.username = "vagrant"
        cfg.ssh.password = "vagrant"
        cfg.vm.box = "bento/ubuntu-20.04"
        cfg.vm.hostname = "malbox-greenhouse-worker2"
        cfg.disksize.size = '250GB'
        #config.vbguest.auto_update = true # virtualbox tools
        cfg.vm.synced_folder ".", "/vagrant"
        cfg.vm.network :private_network, ip: "192.168.38.163", gateway: "192.168.38.1", dns: "8.8.8.8"
        cfg.vm.provision :shell, path: "vagrant/1system.sh"
        cfg.vm.provision :reload #"reload"
        cfg.vm.provision :shell, path: "vagrant/3app.sh", privileged: false
        cfg.vm.provider "virtualbox" do |vb, override|
            vb.gui = true
            vb.name = "malbox-greenhouse-worker2"
            vb.customize ["modifyvm", :id, "--memory", 8192 ] # 30 + 8 * 1024
            vb.customize ["modifyvm", :id, "--cpus", 6]
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




    config.vm.define "malbox-greenhouse-worker3" do |cfg|
        cfg.ssh.username = "vagrant"
        cfg.ssh.password = "vagrant"
        cfg.vm.box = "bento/ubuntu-20.04"
        cfg.vm.hostname = "malbox-greenhouse-worker3"
        cfg.disksize.size = '250GB'
        #config.vbguest.auto_update = true # virtualbox tools
        cfg.vm.synced_folder ".", "/vagrant"
        cfg.vm.network :private_network, ip: "192.168.38.164", gateway: "192.168.38.1", dns: "8.8.8.8"
        cfg.vm.provision :shell, path: "vagrant/1system.sh"
        cfg.vm.provision :reload #"reload"
        cfg.vm.provision :shell, path: "vagrant/3app.sh", privileged: false
        cfg.vm.provider "virtualbox" do |vb, override|
            vb.gui = true
            vb.name = "malbox-greenhouse-worker3"
            vb.customize ["modifyvm", :id, "--memory", 8192 ] # 30 + 8 * 1024
            vb.customize ["modifyvm", :id, "--cpus", 6]
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



    config.vm.define "malbox-greenhouse-worker4" do |cfg|
        cfg.ssh.username = "vagrant"
        cfg.ssh.password = "vagrant"
        cfg.vm.box = "bento/ubuntu-20.04"
        cfg.vm.hostname = "malbox-greenhouse-worker4"
        cfg.disksize.size = '250GB'
        #config.vbguest.auto_update = true # virtualbox tools
        cfg.vm.synced_folder ".", "/vagrant"
        cfg.vm.network :private_network, ip: "192.168.38.165", gateway: "192.168.38.1", dns: "8.8.8.8"
        cfg.vm.provision :shell, path: "vagrant/1system.sh"
        cfg.vm.provision :reload #"reload"
        cfg.vm.provision :shell, path: "vagrant/3app.sh", privileged: false
        cfg.vm.provider "virtualbox" do |vb, override|
            vb.gui = true
            vb.name = "malbox-greenhouse-worker4"
            vb.customize ["modifyvm", :id, "--memory", 8192 ] # 30 + 8 * 1024
            vb.customize ["modifyvm", :id, "--cpus", 6]
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



    config.vm.define "malbox-greenhouse-worker5" do |cfg|
        cfg.ssh.username = "vagrant"
        cfg.ssh.password = "vagrant"
        cfg.vm.box = "bento/ubuntu-20.04"
        cfg.vm.hostname = "malbox-greenhouse-worker5"
        cfg.disksize.size = '200GB'
        #config.vbguest.auto_update = true # virtualbox tools
        cfg.vm.synced_folder ".", "/vagrant"
        cfg.vm.network :private_network, ip: "192.168.38.166", gateway: "192.168.38.1", dns: "8.8.8.8"
        cfg.vm.provision :shell, path: "vagrant/1system.sh"
        cfg.vm.provision :reload #"reload"
        cfg.vm.provision :shell, path: "vagrant/3app.sh", privileged: false
        cfg.vm.provider "virtualbox" do |vb, override|
            vb.gui = true
            vb.name = "malbox-greenhouse-worker5"
            vb.customize ["modifyvm", :id, "--memory", 8192 ] # 30 + 8 * 1024
            vb.customize ["modifyvm", :id, "--cpus", 6]
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
    cfg.vm.provision :shell, path: "vagrant/logger.sh"
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
    end
  end

end

