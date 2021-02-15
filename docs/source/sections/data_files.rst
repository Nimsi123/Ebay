.. _DataFilesRef:

data_files
==========

.. _csv_docs:

****
/CSV
****

Holds the scraped listing data.

- Data is organized with the following column headers.
	``sale_condition, groupA, groupB, groupC, title, price, date``
	
	``sale_condition`` describes whether the item was sold at Auction or Buy It Now
	
	``groupA, groupB, groupC`` describes the categorization set by the user in ``json_queries.py``
	
	``title, price, date`` are all listing details
- Every row in the file corresponds to a unique listing posted on eBay.com

****
/PNG
****

Holds the .png files for the graphed scrape data.

***********
/HTML_Store
***********

Holds the temporary .txt files used during the scraping process.

**********
Client.csv
**********

Maintains a record of the number of API requests. Helps :class:`Client` keep track of which API key to use.

*********************
query_list_export.csv
*********************

Stores the list of categorized queries selected by the user.

***************
json_queries.py
***************

The .py file where the user inputs the categorized queries to track. See :ref:`AddingQueries`.
