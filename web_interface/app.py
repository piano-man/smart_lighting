from flask import Flask, request,render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'lightdb'
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017

#app.config['MONGO_URI'] = 'mongodb://username:password@database_id:port'

mongo = PyMongo(app)

@app.route('/')
def index():
    print("hello")
    return 'Welcome to Smart Lighting Web Interface!'

@app.route('/intensity', methods=['GET', 'POST'])
def intensity():
    light_data = request.get_json()
    #print(light_data['value'])
    #return render_template('index.html')
#    print("hello")
    light =  mongo.db.light_intensity
    light.insert(light_data)
    return 'Intensity Data : %s %s %s' % (light_data['pi_token'], str(light_data['module_no']), str(light_data['intensity']))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
