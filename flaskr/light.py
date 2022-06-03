from flask import (Blueprint, request, jsonify)

from db import get_db

bp = Blueprint('light', __name__)

@bp.route('/light', methods=['GET'])
def get_light():
    all_lights = get_db().execute(
        'SELECT id, timestamp, cage_id, intensity, start, end'
        ' FROM light'
        ' ORDER BY timestamp DESC'
    ).fetchall()
    result = ""
    for row in all_lights:
        result = result + str(row['id']) + " " + str(row['cage_id']) + " " + str(row['intensity'])\
             + " " + str(row['start']) + " " + str(row['end']) + " " + str(row['timestamp']) + "\n"
    return result

@bp.route('/light', methods=['POST'])
def set_light():
    cage_id = request.form['cage_id']
    intensity = request.form['intensity']
    start = request.form['start']
    end = request.form['end']
    error = None

    if not cage_id:
        return jsonify({'status': 'Please enter cage id'}), 403
    elif not intensity:
        return jsonify({'status': 'Please enter intensity'}), 403
    elif not start: 
        return jsonify({'status': 'Please enter start time'}), 403  
    elif not end: 
        return jsonify({'status': 'Please enter stop time'}), 403       

    db = get_db()
    db.execute(
        'INSERT INTO light (cage_id, intensity, start, end)'
        ' VALUES (?, ?, ?, ?)',
        (cage_id, intensity, start, end)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, cage_id, intensity, start, end'
        ' FROM light'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Success',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'cage_id': check['cage_id'],
            'intensity': check['intensity'],
            'start': check['start'],
            'end': check['end']
        }
        }), 200 
@bp.route('/light', methods=['DELETE'])
def delete_light():
    light_id = request.form['id']

    if not light_id:
        return jsonify({'status': 'light id '}), 403
    print(f"light id is {light_id}")

    db = get_db()
    db.execute(
        'DELETE FROM light'
        ' WHERE id=?',
        light_id
    )
    db.commit()
    return jsonify({'status': 'Success'}), 200