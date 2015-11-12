Write your own plugin
*********************

A tourbillon's plugin is a set of collector functions which one has the following signature: ::

	def my_collector(agent):
		pass


The tourbillon agent expose methods to create a database for your metrics, create a retention policy for your database and push your metrics to an influxDB.



Write your collector function as asyncio coroutine
==================================================

To write your collector function as a coroutine you have to decorate your function as follow: ::

	@asyncio.coroutine
	def my_collector(agent):
		pass

Than you need to wait for the agent become ready. You have to access the agent run_event property and wait for the event to be set: ::

	@asyncio.coroutine
	def myplugin(agent):
		yield from agent.run_event.wait()


When the agent as ready, you must create a database to store your measurements. You can also define a retention policy for your metrics:

.. code-block:: python
   :emphasize-lines: 2,3
	
	try:
		yield from agent.async_create_database('mydb')
		yield from agent.async_create_retention_policy('mydb_rp', '365d', '1', 'mydb')
	except:
		pass


.. warning::
	You must surround these steps with a try/except block because they are executed every time the agent starts.



You have to run your collecting metrics loop until the run_event is unset: ::

	while agent.run_event.is_set():
		collect_metric()
		yield from agent.async_push(points, database)
		yield from asyncio.sleep(frequency)	



Write your plugin as a thread target function
=============================================






