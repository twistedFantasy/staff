# Vagrant

## Debian-based Linux distributions

1/ To install Vagrant, you can visit official website and [download](https://www.vagrantup.com/downloads.html) Debian package.
This method allows you to install latest available version of vagrant.
To install vagrant from deb package just use command below:
```
$ sudo apt install ./vagrant_2.2.5_x86_64.deb
```

2/ To create and start new virtual machine which marked as primary(srt) from Vagrantfile
```
$ vagrant up
```

3/ To connect existing virtual machine which marked as primary(srt) by ssh
```
$ vagrant ssh
```

3/ To stop all virtual machine from Vagrantfile
```
$ vagrant halt
```

4/ To delete all existing virtual machine from Vagrantfile
```
$ vagrant destroy
```
