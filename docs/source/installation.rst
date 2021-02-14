Installation and Setup
======================

Run ``pip install eBayScraper`` on the command line.

******************************
Adding queries to a collection
******************************

- Navigate to ``eBayScraper/data_files`` and open ``json_queries.py``
- Add categories and items within categories to the dictionary.
	We represent the ordering of categories and sub-categories as dictionaries.
	Keys are the categories, and you can have sub-categories as values. 
	The nested structure ends when you place a list of queries as the value.

	For example, the code below would be a way of organizing iPhone models within the iPhone 
	category within the Phone category. There can also be other sub-categories to Phones.
	Lastly, there can be either one and two sub-categories. Notice how Apple Watches only have
	one sub-category.

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

	You should note that the **string in the list** is what is actually searched on eBay.