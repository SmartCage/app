from db import get_db
from flask import (Blueprint, jsonify, request)


bp = Blueprint("cage", __name__)

@bp.route("/cage", methods=["GET"])
def get_cage():
    all_cages = get_db().execute(
        'SELECT id, timestamp, default_mode, total_food_quantity, temperature, required_temperature'
        ' FROM cage'
        ' ORDER BY timestamp DESC'
    ).fetchall()
    result = ""
    for row in all_cages:
        result = result + str(row['id']) + " " + str(row['default_mode']) + " " + str(row['total_food_quantity'])+ " " + str(row['temperature']) + " " + str(row['required_temperature']) + " " + str(row['timestamp']) + "\n"
    return result

@bp.route("/cage", methods=["POST"])
def set_cage():
    default_mode = request.form["mode"]
    total_quantity = request.form["total_quant"]
    temperature = request.form ["temperature"]
    required_temperature = request.form ["required_temperature"]
    error = None
    

    if not default_mode:
        return jsonify({'status': 'Please enter desired mode'}), 403
    elif not total_quantity:
        return jsonify({'status': 'Please enter total quantity'}), 403
    elif not temperature:
        return jsonify({'status': 'Please enter temperature'}), 403
    elif not required_temperature:
        return jsonify({'status': 'Please enter required temperature'}), 403

    print(default_mode)
    print(total_quantity)
    print(temperature)
    print(required_temperature)

    db = get_db()
    db.execute(
        'INSERT INTO cage(default_mode, total_food_quantity, temperature, required_temperature)'
        ' VALUES (?, ?, ?, ?)',
        (default_mode, total_quantity, temperature, required_temperature)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, default_mode, total_food_quantity, temperature, required_temperature '
        ' FROM cage'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'cage successfully recorded',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'default_mode': check['default_mode'],
            'total_food_quantity': check['total_food_quantity'],
            'temperature' : check['temperature'],
            'required_temperature' : check['required_temperature']

        }
    }), 200

@bp.route("/cage", methods=["PUT"])
def update_cage():
    
    default_mode = request.form["mode"]
    cage_id = request.form["id"]
    total_food_quantity = request.form["total_quant"]
    temperature = request.form ["temperature"]
    required_temperature = request.form ["required_temperature"]

    if not cage_id:
        return jsonify({'status': 'Please enter cage id'}), 403
    elif not total_food_quantity:
        return jsonify({'status': 'Please enter food quantity'}), 403
    elif not default_mode:
        return jsonify({'status': 'Please enter default mode'}), 403
    elif not temperature:
        return jsonify({'status': 'Please enter temperature'}), 403
    elif not required_temperature:
        return jsonify({'status': 'Please enter required_temperature'}), 403

    print(cage_id)
    print(total_food_quantity)
    print(default_mode)
    print(temperature)
    print(required_temperature)

    db = get_db()
    db.execute(
        'UPDATE cage'
        ' SET default_mode=?, total_food_quantity=?, temperature =?, required_temperature=?,timestamp=CURRENT_TIMESTAMP'
        ' WHERE id=?',
        (default_mode, total_food_quantity, temperature, required_temperature, cage_id)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, default_mode, total_food_quantity, temperature, required_temperature'
        ' FROM cage'
        ' WHERE id=?',
        (cage_id,)
    ).fetchone()
    if not check:
        return jsonify({'status':'cage does not exist'})
    return jsonify({
        'status': 'cage successfully updated',
        'data': {
            'id': check['id'],
            'default_mode': check['default_mode'],
            'total_food_quantity': check['total_food_quantity'],
            'temperature' : check['temperature'],
            'required_temperature' : check['required_temperature']
        }
    }), 200


@bp.route("/cage/<string:_id>", methods=["DELETE"])
def delete_cage(_id):
    if not _id:
        return jsonify({'status': 'Please enter cage id'}), 403
    
    print(_id)

    db = get_db()
    db.execute(
        'DELETE FROM cage'
        ' WHERE id=?',
        (_id,)
    )
    db.commit()

    return jsonify({
        'status': 'cage successfully deleted',
    }), 200