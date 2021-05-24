from eBayScraper.ItemOrganization.query_list import query_list
from eBayScraper.ItemOrganization.Client import Client
from eBayScraper.data_files.queries import d, to_js_json
from eBayScraper.data_files.directories import csv_dir, png_dir

import flask
from flask import request, send_file

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/data', methods=['GET'])
def get_product_data():
	query_name = request.args.get("query")

	totalQueries = query_list(d)
	if not query_name or totalQueries.index_of(query_name) == -1:
		return page_not_found(404)

	return send_file(png_dir(query_name))

app.run()