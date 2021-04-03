.. _ModuleInterfaceRef:

Module Interface
================

Interacting with the scraper, grapher, and web interface can all be achieved at the command line.

Running the scraper
^^^^^^^^^^^^^^^^^^^

- | Running the scraper involves calling ``driver.py`` with command line arguments.
  | See :ref:`cmdline_scrape`.


Graphing the scraping results
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- | Running the grapher involves calling ``driver.py`` with command line arguments.
  | See :ref:`cmdline_graph`.

Viewing graphs with the web interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- | Running the web interface involves calling ``driver.py`` with command line arguments.
  | See :ref:`cmdline_web`.

Example Commands
^^^^^^^^^^^^^^^^

.. code-block:: console

	python driver.py -s 		# Starts the scraper

	python driver.py -s --print 	# Starts the scraper; prints details about the scraping process

	python driver.py --graph 	# Creates graphs from the scraped data

	python driver.py --web 		# Opens the web interface to view graphs

Command Line arguments
^^^^^^^^^^^^^^^^^^^^^^

	.. _cmdline_scrape:

	.. list-table:: Scraping arguments
	   :widths: 25 25
	   :header-rows: 1

	   * - Command line argument
	     - Description
	   * - ``-s``
	     - Scrapes data from eBay.com
	   * - ``-d``
	     - | Performs a deep scrape. The scraper does not stop scraping once it 
	       | reaches a point where the data overlaps from the past.
	   * - ``--synchr``
	     - | Performs a synchronous scrape. This approach does not use 
	       | threading to increase the scraping speed.

	.. _cmdline_graph:

	.. list-table:: Graphing arguments
	   :widths: 25 25
	   :header-rows: 1

	   * - Command line argument
	     - Description
	   * - ``--graph``
	     - | Graphs charts from scraped data. 
	       | Creates .png files in ``eBayScraper/data_files/PNG``

	.. list-table:: Arguments for both scraping and graphing
	   :widths: 25 25
	   :header-rows: 1

	   * - Command line argument
	     - Description
	   * - ``--print``
	     - Prints the progress on either scraping or graphing.
	   * - ``-so``
	     - Only performs one scraping or graphing process.

	.. _cmdline_web:

	.. list-table:: Web interace
	   :widths: 25 25
	   :header-rows: 1

	   * - Command line argument
	     - Description
	   * - ``--web``
	     - Opens up an interactive web page to view the result of your scrapes.
