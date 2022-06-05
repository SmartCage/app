from flask import (Blueprint, request, jsonify)

from db import get_db

bp = Blueprint('parrot_type', __name__)

@bp.route('/parrot_type', methods=['GET'])
def get_parrot_type():
    all_parrot_types = get_db().execute(
        'SELECT *'
        ' FROM parrot_type'
        ' ORDER BY timestamp DESC'
    ).fetchall()
    result = ""
    for row in all_parrot_types:
        result = result + str(row['id']) + " " + str(row['name']) + "  " + str(row['food_id']) + " "\
                 + str(row['min_light_intensity']) + " " + str(row['max_light_intensity']) + " " + str(row['timestamp'])\
                 + "\n"
    return result

@bp.route('/parrot_type', methods=['POST'])
def set_parrot_type():
    type_name = request.form['name']
    min_light_intensity = request.form['min_light_intensity']
    max_light_intensity = request.form['max_light_intensity']
    food_name_id = request.form['food_id']

    if not type_name:
        return jsonify({'status': 'Please enter parrot type name'}), 403
    elif not min_light_intensity:
        return jsonify({'status': 'Please enter parrot type min light'}), 403
    elif not max_light_intensity:
        return jsonify({'status': 'Please enter parrot type max light'}), 403
    elif not food_name_id:
        return jsonify({'status': 'Please enter parrot type food'}), 403

    print(type_name)
    print(min_light_intensity)
    print(max_light_intensity)
    print(food_name_id)
    db = get_db()
    db.execute(
        'INSERT INTO parrot_type (name, food_id, min_light_intensity, max_light_intensity)'
        ' VALUES (?, ?, ?, ?)',
        (type_name, food_name_id, min_light_intensity, max_light_intensity)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, name, food_id, min_light_intensity, max_light_intensity, timestamp'
        ' FROM parrot_type'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Parrot type successfully created',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'name': check['name'],
            'food_id': check['food_id'],
            'min_light': check['min_light_intensity'],
            'max_light': check['max_light_intensity']
        }
    }), 200


@bp.route('/parrot_type', methods=['PUT'])
def update_parrot_type():
    parrot_type_id = request.form['id']
    type_name = request.form['name']
    min_light_intensity = request.form['min_light_intensity']
    max_light_intensity = request.form['max_light_intensity']
    food_name_id = request.form['food_id']

    if not parrot_type_id:
        return jsonify({'status': 'Parrot type id is required.'}), 403
    elif not type_name:
        return jsonify({'status': 'Parrot type name is required.'}), 403
    elif not min_light_intensity:
        return jsonify({'status': 'Parrot type min light intensity is required.'}), 403
    elif not max_light_intensity:
        return jsonify({'status': 'Parrot type max light intensity is required.'}), 403
    elif not food_name_id:
        return jsonify({'status': 'Parrot type food id is required.'}), 403

    print(parrot_type_id)
    print(type_name)
    print(min_light_intensity)
    print(max_light_intensity)
    print(food_name_id)

    db = get_db()
    db.execute(
        'UPDATE parrot_type'
        ' SET name=?, min_light_intensity=?, max_light_intensity=?, food_id=?, timestamp=CURRENT_TIMESTAMP'
        ' WHERE id=?',
        (type_name, min_light_intensity, max_light_intensity, food_name_id, parrot_type_id)
    )
    db.commit()

    check = get_db().execute(
        'SELECT *'
        ' FROM parrot_type'
        ' WHERE id=?',
        (parrot_type_id,)
    ).fetchone()
    if not check:
        return jsonify({'status': 'Parrot type not found'}), 404
    return jsonify({
        'status': 'Parrot type successfully updated',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'name': check['name'],
            'food_id': check['food_id'],
            'min_light': check['min_light_intensity'],
            'max_light': check['max_light_intensity']
        }
    }), 200


@bp.route('/parrot_type/<string:_id>', methods=['DELETE'])
def delete_parrot_type(_id):
    if not _id:
        return jsonify({'status': 'parrot type id is required.'}), 403

    print(_id)

    db = get_db()
    db.execute(
        'DELETE FROM parrot_type'
        ' WHERE id=?',
        (_id,)
    )
    db.commit()

    return jsonify({
        'status': 'parrot type successfully deleted.',
    }), 200 