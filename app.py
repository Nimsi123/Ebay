from eBayScraper.ItemOrganization.query_list import query_list
from eBayScraper.ItemOrganization.Client import Client
from eBayScraper.data_files.queries import d, to_js_json
from eBayScraper.data_files.directories import csv_dir, png_dir

import zipfile
import flask
from flask import request, send_file

app = flask.Flask(__name__)
app.config["DEBUG"] = True

"""
@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
"""

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/data', methods=['GET'])
def get_product_data():
	"""Sends a zip file with the csv file and png file corresponding to scraped 
	data for the 'query' parameter."""
	query_name = request.args.get("query")

	totalQueries = query_list(d)
	if not query_name or totalQueries.index_of(query_name) == -1:
		return page_not_found(404)

	zipfolder = zipfile.ZipFile('Query.zip','w', compression = zipfile.ZIP_STORED) # Compression type 
	zipfolder.write(csv_dir(query_name))
	zipfolder.write(png_dir(query_name))
	zipfolder.close()

	return send_file('Query.zip',
		mimetype = 'zip',
		attachment_filename= 'Query.zip',
		as_attachment = True)

	# Delete the zip file if not needed
	os.remove("Audiofiles.zip")

@app.route('/suggestions', methods=['POST'])
def post_suggestion():
	"""Adds a suggestion (the 'query' parameter) to the query directory."""

app.run()