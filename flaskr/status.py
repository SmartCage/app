from db import get_db

def get_status():
    food_data = get_db().execute(
        'SELECT id, timestamp, type, quantity'
        ' FROM food'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    cage_data = get_db().execute(
        'SELECT id, timestamp, total_food_quantity'
        ' FROM cage'
        ' ORDER BY timestamp DESC'
    ).fetchone()


    light_data = get_db().execute(
    'SELECT id, timestamp, aquarium_id, intensity, color, schedule'
    ' FROM light'
    ' ORDER BY timestamp DESC'
    ).fetchone()

    status = ""
    if food_data is None:
        status += 'The food isn\'t set. '
    elif cage_data is None:
        status += 'The cage isn\'t set. '
    elif light_data is None: 
        status += 'The light isn\'t set.'

    if status != "":
        return {'status': status}

    return {
        'data' : {
        'food': {
                'type': food_data['type'],
                'quantity': food_data['quantity'],
                'timestamp': food_data['timestamp']
        },
        'cage': {
                'total_food_quantity': cage_data['total_food_quantity'],
                'timestamp': cage_data['timestamp']
            },
        'light': {
                'timestamp': light_data['timestamp'],
                'aquarium_id': light_data['aquarium_id'],
                'intensity': light_data['intensity'],
                'color': light_data['color'],
                'schedule': light_data['schedule']
            }

            }
    }
    

    
    