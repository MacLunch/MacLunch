import sys
import json
sys.path.append('../class/')

import Ilwar
from flask import render_template
from flask import request
from flask import Flask
from flask import jsonify

from spamaze_db import DbControl

app = Flask(__name__)
dbcon = DbControl("spamaze")

def load_model():
	predict_model.load_model(save_path = "../predict_model/")

#def make_input(data):
#	return [data]

@app.route('/')
def test_():
	return render_template("test.html")

@app.route('/test')
def home():
	return render_template("index.html")


@app.route('/request', methods = ['POST'])
def send_request():
	data = request.data.decode('utf-8')
	data = json.loads(data)

	print(data)
	
	email = data["email"]
	text = data["message"]

	target_data = ["\"%s\"" % (email), "\"%s\"" % (text)]
	columns = ['email', 'text']
	
	dbcon.insert_data('requests', columns, target_data)

	response = {'status' : 'ok'}
	return jsonify(response)


@app.route('/api/enroll', methods = ['POST'])
def send_enroll():
	data = request.data.decode('utf-8')
	print(data)
	data = json.loads(data)
	print(data)
	
	for item in data:
		content_id = item["id"]
		text = item["text"]
		is_spam = item["is_spam"]
		api_key = item["api_key"]

		target_data = ["\"%s\"" % (content_id), "\"%s\"" % (text), \
						"\"%s\"" % (is_spam), "\"%s\"" % (api_key)]

		columns = ['content_id', 'text', 'is_spam', 'api_key']
	
		dbcon.insert_data('enrolls', columns, target_data)

	response = {'status' : 'ok'}
	return jsonify(response)


@app.route('/api/recognize', methods = ['POST'])
def test():
	data = request.data.decode('utf-8')
	print(data)
	#input_data = make_input(json.loads(data))
	input_data = json.loads(data)

	modify_data = []
	for item in input_data:
		print(item)
		temp_item = item
		temp_item["pk"] = item["id"]
		del temp_item["id"]
		modify_data.append(temp_item)

	print(modify_data)
	result = predict_model.predict(input_data)
	
	response = {}
	for i in range(0, len(input_data)):
		response[str(input_data[i]["pk"])] = bool(result[i])

	return jsonify(response)

if __name__ == '__main__':
	predict_model = Ilwar.TrollClassifier()
	load_model()
	app.run(host="0.0.0.0", port=80, debug=True)
