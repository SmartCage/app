
import random
import pytest
import json



from requests import request
from app import create_app
from db import get_db


"""Initialize the testing environment
Creates an app for testing that has the configuration flag ``TESTING`` set to
``True``.
"""


@pytest.fixture
def client():
    #app.config['TESTING'] = True
    local_app = create_app()
    client = local_app.test_client()

    yield client

def test_root_endpoint(client):
    landing = client.get("/")
    html = landing.data.decode()

    assert 'Hello, World!' in html
    assert landing.status_code == 200


def test_get_cage(client):
    request = client.get("/cage")
    assert request.status_code == 200


def test_set_cage(client):
    payload = {'mode': 'petshop', 'total_quant': 0, 'temperature': 0, 'required_temperature':0}
    rv = client.post('/cage', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "cage successfully recorded"


def test_set_cage_null(client):
    payload = {'mode': 'petshop', 'total_quant': 10, 'temperature': 30, 'required_temperature':''}
    rv = client.post('/cage', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 403
    assert res["status"] == 'Please enter required temperature'


def test_update_cage(client):

    with create_app().app_context():
        cage = get_db().execute(
            'SELECT id'
            ' FROM cage'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    payload = {'id': cage['id'], 'mode': 'petshop', 'total_quant': 20, 'temperature': 5, 'required_temperature':30}
    
    rv = client.put('/cage', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "cage successfully updated"



def test_delete_cage(client):

    with create_app().app_context():
        cage = get_db().execute(
            'SELECT id'
            ' FROM cage'
            ' ORDER BY id DESC'
        ).fetchone()
        print(cage)
    print(str(cage['id']))
    rv = client.delete('/cage/' + str(cage['id']), follow_redirects=True)
    print(rv)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "cage successfully deleted"

def test_get_food(client):
    request = client.get("/food")
    assert request.status_code == 200


def test_set_food(client):
    payload = {'food': 'grains', 'quant': 10}
    rv = client.post('/food', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Food name successfully updated"


def test_set_food_null(client):
    payload = {'food': "", 'quant': 200}
    rv = client.post('/food', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 403
    assert res["status"] == 'Please enter the food name.'


def test_update_food(client):

    with create_app().app_context():
        food = get_db().execute(
            'SELECT id'
            ' FROM food'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    payload = {'id': food['id'], 'food': 'vegetables', 'quant': 15}
    rv = client.put('/food', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Food name successfully updated"


def test_delete_food(client):

    with create_app().app_context():
        food = get_db().execute(
            'SELECT id'
            ' FROM food'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    rv = client.delete('/food/' + str(food['id']), follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Food name successfully deleted"

def test_get_parrot(client):
    request = client.get("/parrot")
    assert request.status_code == 200


def test_set_parrot(client):
    payload = {'name': 'parrot_test', 'health': 100, 'birthday':'13/02/2020', 'type_id':3,'cage_id':2}
    rv = client.post('/parrot', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Parrot successfully created"


def test_set_parrot_null(client):
    payload = {'name': '', 'health': 100, 'birthday':'13/02/2020', 'type_id':3,'cage_id':2}
    rv = client.post('/parrot', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 403
    assert res["status"] == 'Please enter parrot name'


def test_update_parrot(client):

    with create_app().app_context():
        parrot = get_db().execute(
            'SELECT id'
            ' FROM parrot'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    payload = {'id': parrot['id'],'name': 'parrot_test', 'health': 100, 'birthday':'13/02/2020', 'type_id':3,'cage_id':2}
    rv = client.put('/parrot', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Parrot successfully updated"


def test_update_parrot_notfound(client):

    with create_app().app_context():
        parrot = get_db().execute(
            'SELECT id'
            ' FROM parrot'
            ' ORDER BY id DESC'
        ).fetchone()
    payload = {'id': parrot['id'] + 1,'name': 'parrot_test', 'health': 100, 'birthday':'13/02/2020', 'type_id':3,'cage_id':2}
    rv = client.put('/parrot', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 404
    assert res["status"] == "Parrot not found"


def test_delete_parrot(client):

    with create_app().app_context():
        parrot = get_db().execute(
            'SELECT id'
            ' FROM parrot'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    rv = client.delete('/parrot/' + str(parrot['id']), follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "parrot successfully deleted."

def test_get_feeding_schedule(client):
    request = client.get("/feeding_schedule")
    assert request.status_code == 200


def test_set_feeding_schedule(client):
    payload = {'cage_id': 3, 'food_name_id': 4,'schedule':'9;00','available_type_quantity':25}
    rv = client.post('/feeding_schedule', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Feeding schedule successfully recorded."


def test_set_feeding_schedule_null(client):
    payload = {'cage_id': 3, 'food_name_id': 4,'schedule':'','available_type_quantity':25}
    rv = client.post('/feeding_schedule', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 403
    assert res["status"] == 'Schedule is required.'


def test_update_feeding_schedule(client):

    with create_app().app_context():
        feeding_schedule = get_db().execute(
            'SELECT id'
            ' FROM feeding_schedule'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    payload = {'id': feeding_schedule['id'], 'cage_id': 4, 'food_name_id': 6,'schedule':'7:00','available_type_quantity':40}
    rv = client.put('/feeding_schedule', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Feeding schedule successfully updated"


def test_delete_feeding_schedule(client):

    with create_app().app_context():
        feeding_schedule = get_db().execute(
            'SELECT id'
            ' FROM feeding_schedule'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    rv = client.delete('/feeding_schedule/' + str(feeding_schedule['id']), follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Feeding schedule successfully deleted"

def test_get_parrot_type(client):
    request = client.get("/parrot_type")
    assert request.status_code == 200


def test_set_parrot_type(client):
    payload = {'name': 'parrot_type_test', 'food_id': 2, 'min_light_intensity':25, 'max_light_intensity':30}
    rv = client.post('/parrot_type', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Parrot type successfully created"


def test_set_parrot_type_null(client):
    payload = {'name': '', 'food_id': 2, 'min_light_intensity':25, 'max_light_intensity':30}
    rv = client.post('/parrot_type', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 403
    assert res["status"] == 'Please enter parrot type name'


def test_update_parrot_type(client):

    with create_app().app_context():
        parrot_type = get_db().execute(
            'SELECT id'
            ' FROM parrot_type'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    payload = {'id': parrot_type['id'],'name': 'parrot_type_test1', 'food_id': 3, 'min_light_intensity':30, 'max_light_intensity':35}
    rv = client.put('/parrot_type', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Parrot type successfully updated"


def test_update_parrot_type_notfound(client):

    with create_app().app_context():
        parrot_type = get_db().execute(
            'SELECT id'
            ' FROM parrot_type'
            ' ORDER BY id DESC'
        ).fetchone()
    payload = {'id': parrot_type['id'] + 1,'name': 'parrot_type_test2', 'food_id': 1, 'min_light_intensity':30, 'max_light_intensity':35}
    rv = client.put('/parrot_type', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 404
    assert res["status"] == "Parrot type not found"


def test_delete_parrot_type(client):

    with create_app().app_context():
        parrot_type = get_db().execute(
            'SELECT id'
            ' FROM parrot_type'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    rv = client.delete('/parrot_type/' + str(parrot_type['id']), follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "parrot type successfully deleted."

def test_get_light(client):
    request = client.get("/light")
    assert request.status_code == 200


def test_set_light(client):
    payload = {'cage_id': 6, 'intensity': 30, 'start':'07', 'end':'20'}
    rv = client.post('/light', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "light successfully created"


def test_set_light_null(client):
    payload = {'cage_id': 6, 'intensity': '', 'start':'07', 'end':'20'}
    rv = client.post('/light', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 403
    assert res["status"] == 'Please enter intensity'


def test_update_light(client):

    with create_app().app_context():
        light = get_db().execute(
            'SELECT id'
            ' FROM light'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    payload = {'id': light['id'],'cage_id': 6, 'intensity': 35, 'start':'09', 'end':'21'}
    rv = client.put('/light', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "light successfully updated"


def test_update_light_notfound(client):

    with create_app().app_context():
        light = get_db().execute(
            'SELECT id'
            ' FROM light'
            ' ORDER BY id DESC'
        ).fetchone()
    payload = {'id': light['id'] + 1,'cage_id': 6, 'intensity': 35, 'start':'09', 'end':'21'}
    rv = client.put('/light', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 404
    assert res["status"] == "light not found"


def test_delete_light(client):

    with create_app().app_context():
        light = get_db().execute(
            'SELECT id'
            ' FROM light'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    rv = client.delete('/light/' + str(light['id']), follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "light successfully deleted"

def test_get_heat(client):
    request = client.get("/heat")
    assert request.status_code == 200


def test_set_heat(client):
    payload = {'cage_id': 6, 'intensity': 30, 'max_heat' : 60}
    rv = client.post('/heat', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "heat successfully created"


def test_set_heat_null(client):
    payload = {'cage_id': 6, 'intensity': '', 'max_heat' : 60}
    rv = client.post('/heat', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 403
    assert res["status"] == 'Please enter intensity'


def test_update_heat(client):

    with create_app().app_context():
        heat = get_db().execute(
            'SELECT id'
            ' FROM heat'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    payload = {'id': heat['id'],'cage_id': 6, 'intensity': 35, 'max_heat' : 60}
    rv = client.put('/heat', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "heat successfully updated"


def test_update_heat_notfound(client):

    with create_app().app_context():
        heat = get_db().execute(
            'SELECT id'
            ' FROM heat'
            ' ORDER BY id DESC'
        ).fetchone()
    payload = {'id': heat['id'] + 1,'cage_id': 6, 'intensity': 35, 'max_heat' : 60}
    rv = client.put('/heat', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 404
    assert res["status"] == "heat not found"


def test_delete_heat(client):

    with create_app().app_context():
        heat = get_db().execute(
            'SELECT id'
            ' FROM heat'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    rv = client.delete('/heat/' + str(heat['id']), follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "heat successfully deleted"


    