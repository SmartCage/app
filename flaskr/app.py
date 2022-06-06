from flask import Flask
from threading import Thread
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_restful import Api, Resource


import db
import auth
import status
import food
import parrot_type
import cage
import change_light
import facility
import feed
import light_intens
import feeding_schedule
import parrot
import light
import heat
import temperature
import facility
import heat
from heat_data import parse_data, send_data
from change_light import Lightintensity
from cage_mode import CageMode

import eventlet
import json
import time
import os 
eventlet.monkey_patch()
app = None
mqtt = None
socketio = None
thread = None
thread_temp = None
thread_feed = None
thread_light = None


topic = 'python/mqtt'
def create_app(test_config=None):
    
    # create and configure the app
    global app 
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
      
    @app.route('/')
    def hello():
        global thread, thread_temp, thread_feed,  thread_light
        if thread is None:
            thread = Thread(target=background_thread)
            thread.daemon = True
            thread.start()

            thread_temp = Thread(target=thread_temperature)
            thread_temp.daemon = True
            thread_temp.start()

            thread_feed = Thread(target=thread_feed)
            thread_temp.daemon = True
            thread_temp.start

            thread_light = Thread(target=thread_light)
            thread_temp.daemon = True
            thread.start()

        return 'Hello, World!'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(food.bp)
    app.register_blueprint(cage.bp)
    app.register_blueprint(parrot_type.bp)
    app.register_blueprint(feeding_schedule.bp)
    app.register_blueprint(parrot.bp)
    app.register_blueprint(light.bp)
    app.register_blueprint(heat.bp)

    return app

def background_thread():
    count = 0
    while True:
        time.sleep(7)
        with app.app_context():
            message = '\n\nSystem status: \n'
            message += json.dumps(status.get_status(), default=str)
            message += '\n\nUtility notifications:\n'
            message += json.dumps(status.get_utility_status(), default=str)
        mqtt.publish(topic, message)

def create_mqtt_app():
    global app 
    # Setup connection to mqtt broker
    app.config['MQTT_BROKER_URL'] = 'localhost' 
    app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
    app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
    app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
    app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
    app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

    global mqtt
    mqtt = Mqtt(app)
    global socketio 
    socketio = SocketIO(app, async_mode="eventlet")

def thread_feed_parrot():
    while True:
        with app.app_context():
            message = '\n\nFeeding schedule check!\n'
            message += json.dumps(feed.feed_the_parrot(), default=str)
            message += '\n'
        # Publish
        mqtt.publish(topic, message)
        time.sleep(4)

def thread_light():
    while True:
        time.sleep(5)
        with app.app_context():
            message = '\nLight intensity auto-check!\n'
            message += json.dumps(light_intens.light_intensity(), default=str)
            message += '\n'
        # Publish
        mqtt.publish(topic, message)

def tread__heat_data():
    heat_data = parse_data('heat.csv')
    sleepTime = 11
    cage_id = 1
    url = 'http://[::1]:5000/heat'
    send_data(heat_data, cage_id, sleepTime, url)

def create_rest_api(app):

    api = Api(app)
    api.add_resource(CageMode, '/cageMode/<int:id>')
    return api


def run_socketio_app():
    global app 
    create_app()
    create_mqtt_app()
    socketio.run(app, host='localhost', port=5000, use_reloader=False, debug=True)

def thread_temperature():
    while True:
        time.sleep(4)
        with app.app_context():
            message = '\nTemperature auto-check!\n'
            message += json.dumps(temperature.set_temperature(), default=str)
            message += '\n'
        # Publish
        mqtt.publish(topic, message)

if __name__ == '__main__':
    run_socketio_app()