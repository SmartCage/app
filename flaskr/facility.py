from db import get_db
from flask import (Blueprint, jsonify, request)
bp = Blueprint("facility", __name__)

@bp.route("/facility", methods=["GET"])
def get_facility():
    all_facilities = get_db().execute(
        'SELECT *'
        ' FROM facility'
        ' ORDER BY timestamp DESC'
    ).fetchall()
    result = ""
    for row in all_facilities:
        result = result + str(row['id']) + \
                 " electricity:" + str(row['electricity']) \
                 + " movement_sensor:" + str(row['movement_sensor']) \
                 + " temperature_sensor" + str(row['temperature_sensor']) \
                 + " cage_id:" + str(row['cage_id']) \
                 + " " + str(row['timestamp']) \
                 + "\n"
    return result
@bp.route('/facility', methods=["POST"])
def set_facility():
    electricity = request.form['electricity']
    movement_sensor = request.form['movement_sensor']
    temperature_sensor = request.form['temperature_sensor']
    cage_id = request.form['cage_id']
    if not electricity:
        return jsonify({'status': 'Electricity status is required.'}), 403
    elif not movement_sensor:
        return jsonify({'status': 'Movement sensor status is required.'}), 403
    elif not temperature_sensor:
        return jsonify({'status: Temperature sensor status is required.'}), 403
    elif not cage_id:
        return jsonify({'status: cage_id is required.'}), 403
    print(f"electricity status is {electricity}")
    print(f"movement_sensor status is {movement_sensor}")
    print(f"temperature_sensor status is {temperature_sensor}")
    print(f"cage_id is {cage_id}")
    db = get_db()
    db.execute('INSERT INTO facility (cage_id, electricity, movement_sensor, temperature_sensor) '
               ' VALUES (?, ?, ?, ?)',
               (cage_id, electricity, movement_sensor, temperature_sensor)
               )
    db.commit()

    check = get_db().execute(
        'SELECT id, cage_id, electricity, movement_sensor, temperature_sensor, '
        'timestamp '
        ' FROM facility'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    return jsonify({
        'status': 'New facility list successfully recorded',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'cage_id': check['cage_id'],
            'electricity': check['electricity'],
            'movement_sensor': check['movement_sensor'],
            'temperature_sensor': check['temperature_sensor']
        }
    }), 200


@bp.route('/facility', methods=['PUT'])
def update_facility():

    electricity = request.form['electricity']
    movement_sensor = request.form['movement_sensor']
    temperature_sensor = request.form['temperature_sensor']
    cage_id = request.form['cage_id']
    facility_id = request.form['id']


    if not facility_id:
        return jsonify({'status': 'Facility id is required.'}), 403
    elif not electricity:
        return jsonify({'status': 'Electricity status is required.'}), 403
    elif not movement_sensor:
        return jsonify({'status': 'Movement sensor status is required.'}), 403
    elif not temperature_sensor:
        return jsonify({'status: Temperature sensor status is required.'}), 403
    elif not cage_id:
        return jsonify({'status: cage_id is required.'}), 403

    print(f"electricity status is {electricity}")
    print(f"movement_sensor status is {movement_sensor}")
    print(f"temperature_sensor status is {temperature_sensor}")
    print(f"cage_id is {cage_id}")

    db = get_db()
    db.execute('UPDATE facility'
               ' SET electricity=?, movement_sensor=?, temperature_sensor=?, '
               'cage_id=?, timestamp = CURRENT_TIMESTAMP '
               ' WHERE id=?',
               (electricity, movement_sensor, temperature_sensor, cage_id, facility_id)
               )
    db.commit()

    check = get_db().execute(
        'SELECT *'
        ' FROM facility'
        ' WHERE id=?',
        facility_id
        (facility_id,)
    ).fetchone()

    if not check:
        return  jsonify({'statu': 'List does not exist. '}), 404

    return jsonify({
        'status': 'Facility list was updated',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'cage_id': check['cage_id'],
            'electricity': check['electricity'],
            'movement_sensor': check['movement_sensor'],
            'weight_sensor': check['weight_sensor']
        }
    }), 200


@bp.route('/facility/<string:_id>', methods=['DELETE'])
def delete_facility(_id):
    if not _id:
        return jsonify({'status': 'Facility id is required.'}), 403

    print(_id)

    db = get_db()
    db.execute(
        'DELETE FROM facility'
        ' WHERE id=?',
        (_id,)
    )
    db.commit()

    return jsonify({'status': 'Facility list successfully deleted'}), 200