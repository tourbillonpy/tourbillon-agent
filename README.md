![image](https://raw.githubusercontent.com/tourbillonpy/tourbillon-agent/master/assets/tourbillon_logo_gray.png) 
#### A Python agent for collecting metrics and store them into an InfluxDB.

-----






# What is tourbillon

tourbillon is an efficient, very simple and extensible agent that allows to collect metrics from servers or services and writes them into a InfluxDB.

It's is written in pure python.

# Supported platforms

tourbillon has been tested and it runs on Ubuntu 12.04 or greater, Centos 6 or greater and Mac OSX Maveriks or greater.
 
tourbillon works under python 2.7 and python 3.4 or greater.

# Documentation

You can browse the tourbillon documentation online, it is hosted on Read The Docs.
The documentation of the latest version of tourbillon can be found here.


# Getting started

## Requirements

There are no special requirements to run tourbillon.

## Installation

### Using distribution packages

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
_It's strongly recomended to install tourbillon inside a virtualenv._

```
$ pip install tourbillon
```


## Generate an initial configuration file

Except for the debian package, you will need to generate the tourbillon's configuration file.

By default, the tourbillon's configuration is stored in **/etc/tourbillon/tourbillon.conf**.

To generate the configuration file type the following command:

```
$ tourbillon init
````

The init command will ask you for the InfluxDB's connection parameters and the logging configuration.



## List available Tourbillon plugins
tourbillon has an index of official, featured and unofficial plugins.
The plugins listed in the index are python packages hosted on pypi.

You can list the plugins present in the index by typing:

```
$ tourbillon list
```

The output of this command will only show the plugins compatible with you python runtime version.


## Plugins installation

To install a plugin enter:

```
$ tourbillon install <plugin-name>
```

After the installation it will be needed to create the plugin configuration file.
By default tourbillon search for the plugins configuration file in **/etc/tourbillon/conf.d**.
Please refer to the plugin documentation for detailed instruction.



# Usage

blah blah

# Contributing

blah blah


# Credits

* Alba Vilardebò, logo designer, [albavilardebo.com](http://albavilardebo.com).


# License

tourbillon and all the official plugins are released under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).








