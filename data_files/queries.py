d = {
	"calculator": ["ti-83 plus calculator", "ti-84 plus calculator", "ti-84 plus CE calculator", "ti-89 calculator"]
}


def to_js_json():
    """Converts all of the queries inputted by the user into a javascript file.
    """
    from eBayScraper.data_files.directories import JS_JSON_DIR
    import json

    with open(JS_JSON_DIR, "w") as file:
        file.write("var d = " + json.dumps(d) + ";")