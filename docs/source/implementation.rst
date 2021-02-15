========================================
Underlying Data Structure Implementation
========================================

************************
Pandas and ``DataFrame``
************************

eBayScraper uses pandas' ``DataFrame`` module to manipulate the scraped listing data.

- You can recreate this object by importing from a csv file

	.. code-block:: python
		:linenos:

		pd.read_csv(csv_file)

The ``DataFrame`` object can be described by 

	.. code-block:: python
		:linenos:

		pd.DataFrame(columns = ["sale_condition", "groupA", "groupB", "groupC", "title", "price", "date"])