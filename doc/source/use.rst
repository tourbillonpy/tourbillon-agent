Use tourbillon
**************


Command Line Interface (CLI)
============================

The available CLI commands are:

	* **init**: generate an initial configuraton file
	* **list**: list all available plugins for tourbillon included in the tourbillon plugins index.
	* **install**: install a tourbillon-plugin
	* **upgrade**: upgrade a tourbillon-plugin
	* **reinstall**: reinstall a tourbillon-plugin
	* **enable**: enable one or more collector functions
	* **disable**: disable one or more collector functions
	* **show**: show the list of enabled plugins
	* **clear**: disable all plugins
	* **run**: runs tourbillon



List available plugins
----------------------

To list all the available plugins for tourbillon types: ::

	$ tourbillon list

The list command output looks like:

+--------------------+-----+------------------------------------------------------------+-----------------------------------+-+
|name                |ver. |description                                                 |author                             |F|
+====================+=====+============================================================+===================================+=+
|tourbillon-uwsgi    |0.2  |tourbillon uwsgi plugin                                     |The Tourbillon Team                |*|
+--------------------+-----+------------------------------------------------------------+-----------------------------------+-+
|tourbillon-linux    |0.2  |tourbillon linux plugin                                     |The Tourbillon Team                |*|
+--------------------+-----+------------------------------------------------------------+-----------------------------------+-+


