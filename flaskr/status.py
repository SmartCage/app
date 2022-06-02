from db import get_db

def get_status():
    food_data = get_db().execute(
        'SELECT id, timestamp, type, quantity'
        ' FROM food'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    cage_data = get_db().execute(
        'SELECT id, timestamp, default_mode, total_food_quantity'
        ' FROM cage'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    status = ""
    if food_data is None:
        status += 'The food isn\'t set. '
    elif cage_data is None:
        status += 'The cage isn\'t set. '
    
    if status != "":
        return {'status': status}

    return {
        'food': {
                'type': food_data['type'],
                'quantity': food_data['quantity'],
                'timestamp': food_data['timestamp']
        },
        'cage': {
                'default_mode': cage_data['default_mode'],
                'total_food_quantity': cage_data['total_food_quantity'],
                'timestamp': cage_data['timestamp']
            }

    }
    