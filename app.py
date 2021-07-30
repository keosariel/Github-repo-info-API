from flask import (
	Flask, 
	request,
	jsonify,
	render_template
)
from utils import get_repo_info

app = Flask(__name__)

def json_response(data, has_error=False, description="", status=200):
	return jsonify(
		{
			"data": data,
			"has_error": has_error,
			"description":description,
			"status":status
		}
	)

@app.route("/", methods=["GET"])
def home():
	return render_template("index.html")

@app.route("/repo", methods=["GET"])
def get_info():
	url = request.args.get("url")	

	if url:
		repo_info = get_repo_info(url)
		return jsonify(data=repo_info)

	return json_response(
		data=None, 
		has_error=True, 
		description="No url given"
	)

if __name__ == "__main__":
	app.run(debug=True)