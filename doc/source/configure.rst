Configure
*********


Generate an initial configuration file
======================================


Except for the debian package, you will need to generate the tourbillon's configuration file.

By default, the tourbillon's configuration is stored in **/etc/tourbillon/tourbillon.conf**.

To generate the configuration file type the following command: ::

	$ tourbillon init


The init command will ask you for the InfluxDB's connection parameters and the logging configuration.


tourbillon.conf
===============

.. note::
	Generally, it is not required to modify the tourbillon cofiguration file manually.


The tourbillon configuration file looks like: ::

	{
	  "database": {
	    "host": "localhost", 
	    "port": 8086
	  }, 
	  "log_format": "%(asctime)s %(levelname)s [%(name)s %(filename)s:%(funcName)s:%(lineno)d] %(message)s", 
	  "log_level": "DEBUG", 
	  "plugins": {
	    "tourbillon.celery": [
	      "get_celery_stats"
	    ]
	  }, 
	  "plugins_conf_dir": "${tourbillon_conf_dir}/conf.d"
	}



* **database**: InfluxDB configuration section
	* **host**: hostname or ip address of the InfluxDB instance
	* **port**: port at which InfluxDB is listening to
	* **username**: database username (optional)
	* **password**: database user password (optional)
* **log_format**: logfile format (see python logging)
* **log_level**: log level (see python logging)
* **plugins**: tourbillon plugins configuration section
* **plugins_conf_dir**: directory where tourbillon search for the plugins configuration files.


