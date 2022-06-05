from flask import (Blueprint, request, jsonify)

from db import get_db

bp = Blueprint('heat', __name__)

@bp.route('/heat', methods=['GET'])
def get_heat():
    all_heats = get_db().execute(
        'SELECT id, timestamp, cage_id, intensity, max_heat'
        ' FROM heat'
        ' ORDER BY timestamp DESC'
    ).fetchall()
    result = ""
    for row in all_heats:
        result = result + str(row['id']) + " " + str(row['cage_id']) + " " + str(row['intensity'])\
             + " " + str(row['max_heat']) + " " + str(row['timestamp']) + "\n"
    return result

@bp.route('/heat', methods=['POST'])
def set_heat():
    cage_id = request.form['cage_id']
    intensity = request.form['intensity']
    max_heat = request.form['max_heat']
    error = None

    if not cage_id:
        return jsonify({'status': 'Please enter cage id'}), 403
    elif not intensity:
        return jsonify({'status': 'Please enter intensity'}), 403
    elif not max_heat: 
        return jsonify({'status': 'Please enter max heat '}), 403       
 
    db = get_db()
    db.execute(
        'INSERT INTO heat (cage_id, intensity, max_heat)'
        ' VALUES (?, ?, ?)',
        (cage_id, intensity, max_heat)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, cage_id, intensity, max_heat'
        ' FROM heat'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'heat successfully created',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'cage_id': check['cage_id'],
            'intensity': check['intensity'],
            'max_heat': check['max_heat']
            
        }
        }), 200 

@bp.route('/heat', methods=['PUT'])
def update_heat():
    heat_id = request.form['id']
    cage_id = request.form['cage_id']
    intensity = request.form['intensity']
    max_heat = request.form['max_heat']
    
    if not heat_id:
        return jsonify({'status': 'Please enter heat id'}), 403
    if not cage_id:
        return jsonify({'status': 'Please enter cage id'}), 403
    elif not intensity:
        return jsonify({'status': 'Please enter intensity'}), 403
    elif not max_heat: 
        return jsonify({'status': 'Please enter max heat'}), 403  


    db = get_db()
    db.execute(
        'UPDATE heat'
        ' SET cage_id=?, intensity=?, max_heat=?, timestamp=CURRENT_TIMESTAMP'
        ' WHERE id=?',
        (cage_id, intensity, max_heat, heat_id)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, cage_id, intensity, max_heat, timestamp'
        ' FROM heat'
        ' WHERE id=?',
        (heat_id,)
    ).fetchone()

    if not check:
        return jsonify({'status': 'heat not found'}), 404

    return jsonify({
        'status': 'heat successfully updated',
        'data': {
            'id': check['id'],
            'cage_id': check['cage_id'],
            'intensity': check['intensity'],
            'max_heat': check['max_heat'],
            'timestamp': check['timestamp']
        }
    }), 200

@bp.route('/heat/<string:_id>', methods=['DELETE'])
def delete_heat(_id):

    if not _id:
        return jsonify({'status': 'heat id is required '}), 403
    print(_id)

    db = get_db()
    db.execute(
        'DELETE FROM heat'
        ' WHERE id=?',
        (_id,)
    )
    db.commit()
    return jsonify({'status': 'heat successfully deleted'}), 200