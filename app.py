from flask import Flask
from utils.DataLoader import DataLoader

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/data', methods=["GET"])
def getData():
    dataLoader = DataLoader("dataset4")
    data, _, _ = dataLoader.getData(["sick", "healthy"], ["LUAD"])
    return 'Shape: '+str(data.shape)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', use_reloader=True)
