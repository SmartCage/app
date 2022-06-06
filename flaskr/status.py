from db import get_db


def get_status():
    food_data = get_db().execute(
        'SELECT id, timestamp, name_food, quantity'
        ' FROM food'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    cage_data = get_db().execute(
        'SELECT id, timestamp, mode, total_food_quantity, temperature, required_temperature'
        ' FROM cage'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    light_data = get_db().execute(
        'SELECT id, timestamp, cage_id, intensity, start_light, end_light'
        ' FROM light'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    status = ""
    if food_data is None:
        status += 'You forgot to set food data. '
    elif cage_data is None:
        status += 'You forgot to set cage data. '
    elif light_data is None:
        status += 'You forgot to set light data.'

    if status != "":
        return {'status': status}

    return {
        'data': {
            'food': {
                'name_food': food_data['name_food'],
                'quantity': food_data['quantity'],
                'timestamp': food_data['timestamp']
            },
            'cage': {
                'mode': cage_data['mode'],
                'total_food_quantity': cage_data['total_food_quantity'],
                'temperature': cage_data['temperature'],
                'required_temperature': cage_data['required_temperature'],
                'timestamp': cage_data['timestamp']
            },
            'light': {
                # 'id': light_data['id'],
                'timestamp': light_data['timestamp'],
                'cage_id': light_data['cage_id'],
                'intensity': light_data['intensity'],
                'start_light': light_data['start_light'],
                'end_light': light_data['end_light']
            }

        }
    }


def get_utility_status():
    mesg = "Warning!  "
    facilities = get_db().execute(
        'SELECT DISTINCT cage_id, electricity, movement_sensor, temperature_sensor'
        ' FROM facility'
    ).fetchall()
    issues = 0
    if facilities is not None:
        for f in facilities:
            if f['electricity'] != 1:
                mesg += f"-Electricity in cage {f['cage_id']} seems to not working, Please fix it!-"
                issues += 1
            elif f['movement_sensor'] != 1:
                mesg += f"-Moveement sensor in cage {f['cage_id']} seems to not working. Please fix it!-"
                issues += 1
            elif f['temperature_sensor'] != 1:
                mesg += f"-Temperature sensor in cage {f['cage_id']} seems to not working. Please fix it!-"
                issues += 1
            if issues == 0:
                mesg += f"Everything in cage {f['cage_id']} seems to be fine!"
    return {'utility_status': mesg}
