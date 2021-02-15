Folder structure
================

eBayScraper's folder structure

| eBayScraper
| └── :ref:`ItemOrganizationRef`
| │   ├── :ref:`ClientRef`
| │   ├── :ref:`ProductCollectionRef`
| │   ├── :ref:`QueryListRef`
| ├── :ref:`SiteOperationsRef`
| │   └── :ref:`AboutALinkRef`
| │   └── :ref:`CleanEntriesRef`
| │   └── :ref:`FastDownloadRef`
| │   └── :ref:`PrinterRef`
| │   └── :ref:`TraverseHTMLRef`
| └── :ref:`DataFilesRef`
|

In the folder structure above:

- ``eBayScraper`` is the folder we get when we issue a ``pip install eBayScraper`` command
- ``eBayScraper/ItemOrganization`` holds scripts that dictate the state of values at run-time. Such values are the scraping client's current api key, the data structure that stores and graphs the listing data, and the class that coordinates the flow of events.
- ``eBayScraper/SiteOperations`` holds scripts that deal with scraping meaningful data from the HTML code.
- ``eBayScraper/data_files`` holds files and folder that pertain to the data to scrape. We store the collection of query names, the API call count, the scraped item data for each query, and the graphed images.