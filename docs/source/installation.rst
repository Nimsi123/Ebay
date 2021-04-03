Installation and Setup
======================

Installation
************

Clone the repository `here <https://github.com/Nimsi123/eBayScraper>`_.

Move the folder to the ``/Python/Python39/`` directory, or the equivalent for your version of Python.

Setup
*****

We will only be working within ``eBayScraper/data_files`` for the setup.

Adding ScraperAPI api keys
^^^^^^^^^^^^^^^^^^^^^^^^^^

eBayScraper relies on ScraperAPI for retrieving eBay HTML. 

#. Start a free-trial with `ScraperAPI <https://www.scraperapi.com/>`_.
#. Open ``data_files/api_keys.py``. Add the api key as a string to the list ``api_keys``. You can add multiple api keys; if an api key reaches its request limit, eBayScraper will switch to another api key.

	Within ``api_keys.py``, this would look like

	.. code-block:: python
		:linenos:

		api_keys = [
			"<add api key>",
			"<optionally add more keys to the list>"
		]


.. _AddingQueries:

Adding queries to a collection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Open ``data_files/queries.py``
- Add categorized search queries to the dictionary.
	We represent the ordering of categories and sub-categories as dictionaries.
	The nested structure ends when you place a list of queries as the value.

	For example, the code below organizes *iPhone models* within the *iPhone* sub-category within the *Phone* category. 
	There can also be other sub-categories within *Phones* at the same hierarchical level as *iPhones*, like *Samsung Galaxy*.
	
	Lastly, there doesn't have to be a sub-category within a category. For example, the category *Apple Watch* does not have sub-categories.

	.. code-block:: python
		:linenos:

		{
			"Phones": {
				"iPhones": ["iPhone6", "iPhone7"],
				"Samsung Galaxy": ["Samsung Galaxy S7 Edge"]
			},
			"Apple Watch": [
				"Apple Watch Series 1", "Apple Watch Series 3", "Apple Watch Series 4", 
				"Apple Watch Series 5", "Apple Watch Series 6", "Apple Watch SE", 
				"Apple Watch Nike", "Apple Watch Hermes"
			]
		}

	- Note
		- The **string in the list** is what you would type into the eBay search bar.
		- You can add and remove from this dictionary at any time!

When you have entered values for the list in ``data_files/api_keys.py`` and the dictionary in
``data_files/queries.py``, run the following command in the terminal to confirm a successful setup.

.. code-block:: console
	
	python driver.py --setup

Move on when the terminal prints **Setup is successful**.

Using the Module
^^^^^^^^^^^^^^^^

**Congratulations!** You're now ready to use all of the features eBayScraper has to offer!
See :ref:`ModuleInterfaceRef` on how to get started!