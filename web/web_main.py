import sys
import json
sys.path.append('../class/')

import Ilwar
from flask import render_template
from flask import request
from flask import Flask
from flask import jsonify

app = Flask(__name__)

def load_model():
	predict_model.load_model(save_path = "../predict_model/")

def make_input(data):
	return [data]

@app.route('/test')
def test_():
	return render_template("test.html")

@app.route('/')
def home():
	return render_template("index.html")

@app.route('/query', methods = ['POST'])
def test():
	data = request.data.decode('utf-8')
	input_data = make_input(json.loads(data))

	result = predict_model.predict(input_data)
	
	response = {}
	for i in range(0, len(input_data)):
		response[str(input_data[i]["pk"])] = bool(result[i])

	return jsonify(response)

if __name__ == '__main__':
	predict_model = Ilwar.TrollClassifier()
	load_model()
	app.run(debug=True)
