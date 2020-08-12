from setuptools import setup

setup(name='eBayItemScraper',
      version='1.0',
      description='Web Scraping Tools for eBay',
      url='http://github.com',
      author='Nima Rahmanian',
      author_email='nimarahmanian8@gmail.com',
      packages=["Book_Scraping", "Device_Scraping",  "Drivers",
                "General_Purpose", "School_Scraping", "Site_Operations"],
      zip_safe=False,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.rst"]
        # And include any *.msg files found in the "hello" package, too:
        #"hello": ["*.msg"],
      }
      
      )
