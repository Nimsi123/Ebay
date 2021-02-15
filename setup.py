from setuptools import setup

setup(name='eBayScraper',
      version='1.0',
      description='An easy way to track listing data for multiple search queries sold on eBay.com.',
      url='http://github.com',
      author='Nima Rahmanian',
      author_email='nimarahmanian8@gmail.com',
      packages=["data_files", "ItemOrganization", "SiteOperations"],
      zip_safe=False,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.rst"]
        # And include any *.msg files found in the "hello" package, too:
        #"hello": ["*.msg"],
      }
      
      )
