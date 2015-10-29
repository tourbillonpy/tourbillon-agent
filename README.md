-> ![image](https://raw.githubusercontent.com/tourbillonpy/tourbillon-agent/master/assets/tourbillon_logo_gray.png) <-
A Python agent for collecting metrics and store them into an InfluxDB.
-----
-----






# What is tourbillon


dadfadf
fad
fad


# Supported platforms

turbillon has been tested and is known to run on Ubuntu 12.04 or greater, Centos 6 or greater and Mac OSX Maveriks or greater.
 
Tourbillon will work under python 2.7 and python 3.4 or greater.

# Documentation

You can browse the tourbillon documentation online, it is hosted on Read The Docs.
The documentation for the latest version of Tourbillon can be found here.


# Getting started

## Requirements

There are no special requirements to run tourbillon.

## Install

### Use distribution packages

#### Debian/Ubuntu

Download the debian package for your architecture:


[tourbillon_0.4_amd64.deb](http://)

[tourbillon_0.4_i386.deb](http://)

Run dpkg to install it:

```
$ sudo dpkg -i tourbillon_0.4_amd64.deb

```

or for the 32 bit version:

```
$ sudo dpkg -i tourbillon_0.4_i386.deb

```



#### RHEL/Centos


Download the rpm package for your architecture:


[tourbillon-0.4-1.x86_64.rpm](http://)

[tourbillon-0.4-1.i386.rpm](http://)


Run rpm to install it:

```
$ sudo rpm -i tourbillon-0.4-1.x86_64.rpm

```

or for the 32 bit version:

```
$ sudo rpm -i tourbillon-0.4-1.i386.rpm

```



### Install with pip
_It's strongly recomended to install Tourbillon within a virtualenv._

```
$ pip install tourbillon
```


## Generate an initial configuration file

Except for the debian package, you will need to generate the tourbillon configuration file.

By default the tourbillon configuration is stored in /etc/tourbillon/tourbillon.conf.

To generate the configuration file runs:

```
$ tourbillon init
````

The init command ask you for the InfluxDB connection parameters and the logging configuration.



## List available Tourbillon plugins
tourbillon have an index of official, featured and unofficial plugins.
The plugins listed in the index python packages hosted on pypi.

You can list the plugins present in the index with:

```
$ tourbillon list
```

tourbillon filter the index with your python version, so if a plugin can only runs on python 2.7 it  will be removed from the list and cannot be installed if you are running python 3.4 or greater.


## Install some plugins

To install tourbillon plugin you have to run:

```
$ tourbillon install <plugin-name>
```

After the installation you need to create the plugin configuration file.
By default it has to be placed in /etc/tourbillon/conf.d.
Please refer to each plugin documentation for detailed instruction.








