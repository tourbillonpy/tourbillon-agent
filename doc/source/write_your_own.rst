Write your own plugin
*********************

A Tourbillon's plugin is a function that has the following signature: ::

	def myplugin(agent):
		pass


The Tourbillon agent expose methods to create a database and a retention policy for your metrics, and push your metrics to an influxDB.


Write your plugin as asyncio coroutine
======================================

To write your plugin as a coroutine you have to decorate your function as follow: ::

	@asyncio.coroutine
	def myplugin(agent):
		pass

Than you need to wait for the agent becomes ready. You have to access the agent run_event property and wait for the event to be set:

.. code-block:: python
	:emphasize-lines: 3,3
	:linenos:

	@asyncio.coroutine
	def myplugin(agent):
		yield from agent.run_event.wait()

After that you must retrieve the configuration parameters for your plugin:

.. code-block:: python
	:emphasize-lines: 4,4
	:linenos:

	@asyncio.coroutine
	def myplugin(agent):
		yield from agent.run_event.wait()
		config = agent.config['myplugin_config_file']

.. note::
	``myplugin_config_file`` is the name of your plugin's configuration file without the ``.conf`` extension.


Next you have to get the database and retention policy parameters from your configuration file:


.. code-block:: python
	:emphasize-lines: 5,5
	:linenos:

	@asyncio.coroutine
	def myplugin(agent):
		yield from agent.run_event.wait()
		config = agent.config['myplugin_config_file']
		db_config = config['database']


And then you are ready to create your database and retention policy in your influxDB instance:

.. code-block:: python
	:emphasize-lines: 6,6
	:linenos:

	@asyncio.coroutine
	def myplugin(agent):
		yield from agent.run_event.wait()
		config = agent.config['myplugin_config_file']
		db_config = config['database']
		yield from agent.async_create_database(**db_config)


Now you can create your metric collector loop:

.. code-block:: python
	:emphasize-lines: 7,8
	:linenos:

	@asyncio.coroutine
	def myplugin(agent):
		yield from agent.run_event.wait()
		config = agent.config['myplugin_config_file']
		db_config = config['database']
		yield from agent.async_create_database(**db_config)
		while agent.run_event.is_set():
			pass


Replace the ``pass`` statement on line 8 with your metric gathering logic. Sleep some time between iterations yielding from	``asyncio.sleep`` function.

.. note::
	tourbillon uses `trollius <https://pypi.python.org/pypi/trollius>`_ for asyncio in python 2.7.
	If you are writing your coroutine for python 2.7 please refers to the Trollius documentation.



Write your plugin as a thread target function
=============================================

To write a plugin as a thread target function follow this steps:

Create your thread target function: ::

	def myplugin(agent):
		pass

Wait for the agent becomes ready. You have to access the agent run_event property and wait for the event to be set:

.. code-block:: python
	:emphasize-lines: 2,2
	:linenos:

	def myplugin(agent):
		agent.run_event.wait()

Retrieve the configuration parameters for your plugin:

.. code-block:: python
	:emphasize-lines: 3,3
	:linenos:

	def myplugin(agent):
		agent.run_event.wait()
		config = agent.config['myplugin_config_file']

.. note::
	``myplugin_config_file`` is the name of your plugin's configuration file without the ``.conf`` extension.


Get the database and retention policy parameters from your configuration file:


.. code-block:: python
	:emphasize-lines: 4,4
	:linenos:

	def myplugin(agent):
		agent.run_event.wait()
		config = agent.config['myplugin_config_file']
		db_config = config['database']


Create your database and retention policy in your influxDB instance:

.. code-block:: python
	:emphasize-lines: 5,5
	:linenos:

	def myplugin(agent):
		agent.run_event.wait()
		config = agent.config['myplugin_config_file']
		db_config = config['database']
		agent.create_database(**db_config)


Create your metric collector loop:

.. code-block:: python
	:emphasize-lines: 6,7
	:linenos:

	def myplugin(agent):
		agent.run_event.wait()
		config = agent.config['myplugin_config_file']
		db_config = config['database']
		agent.create_database(**db_config)
		while agent.run_event.is_set():
			pass


Replace the ``pass`` statement on line 7 with your metric gathering logic. Sleep some time between iterations using ``time.sleep``.







