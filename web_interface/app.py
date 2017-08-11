from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'lightdb'
app.config['MONGO_URI'] = 'mongodb://username:password@database_id:port'

mongo = PyMongo(app)

@app.route('/')
def index():
    return 'Welcome to Smart Lighting Web Interface!'

@app.route('/intensity', methods=['GET', 'POST'])
def intensity():
    light_data = request.get_json()
    light =  mongo.db.light
    light.insert(light_data)
    return 'Intensity Data : %s %s %s' % (light_data['pi_token'], str(light_data['module_no']), str(light_data['intensity']))

if __name__ == '__main__':
    app.run(debug=True)
