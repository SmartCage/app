from db import get_db
from flask import (Blueprint, jsonify, request)


bp = Blueprint("cage", __name__)

@bp.route("/cage", methods=["GET"])
def get_cage():
    all_cages = get_db().execute(
        'SELECT id, timestamp, total_food_quantity, temperature, required_temperature, mode'
        ' FROM cage'
        ' ORDER BY timestamp DESC'
    ).fetchall()
    result = ""
    for row in all_cages:
        result = result + str(row['id']) + " " +  str(row['total_food_quantity'])+ " " + str(row['temperature']) + " " + str(row['required_temperature']) + " " + str(row['timestamp']) + " " + str(row['mode']) +"\n"
    return result

@bp.route("/cage", methods=["POST"])
def set_cage():
    total_quantity = request.form["total_quant"]
    temperature = request.form ["temperature"]
    required_temperature = request.form ["required_temperature"]
    mode = request.form ["mode"]
    error = None
    
    if not total_quantity:
        return jsonify({'status': 'Please enter total quantity'}), 403
    elif not temperature:
        return jsonify({'status': 'Please enter temperature'}), 403
    elif not required_temperature:
        return jsonify({'status': 'Please enter required temperature'}), 403
    elif not mode:
        return jsonify({'status': 'Please enter mode'}), 403


    print(total_quantity)
    print(temperature)
    print(required_temperature)
    print(mode)

    db = get_db()
    db.execute(
        'INSERT INTO cage( total_food_quantity, temperature, required_temperature), mode'
        ' VALUES (?, ?, ?, ?)',
        ( total_quantity, temperature, required_temperature, mode)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, timestamp,  total_food_quantity, temperature, required_temperature, mode '
        ' FROM cage'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'cage successfully recorded',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'total_food_quantity': check['total_food_quantity'],
            'temperature' : check['temperature'],
            'required_temperature' : check['required_temperature'],
            'mode' : check['mode']

    }
    }), 200

@bp.route("/cage", methods=["PUT"])
def update_cage():
    
    cage_id = request.form["id"]
    total_food_quantity = request.form["total_quant"]
    temperature = request.form ["temperature"]
    required_temperature = request.form ["required_temperature"]
    mode = request.form ["mode"]

    if not cage_id:
        return jsonify({'status': 'Please enter cage id'}), 403
    elif not total_food_quantity:
        return jsonify({'status': 'Please enter food quantity'}), 403
    elif not temperature:
        return jsonify({'status': 'Please enter temperature'}), 403
    elif not required_temperature:
        return jsonify({'status': 'Please enter required_temperature'}), 403
    elif not mode:
        return jsonify({'status' : 'Please enter mode'})

    print(cage_id)
    print(total_food_quantity)
    print(temperature)
    print(required_temperature)
    print(mode)

    db = get_db()
    db.execute(
        'UPDATE cage'
        ' SET  total_food_quantity=?, temperature =?, required_temperature=?, mode=?, timestamp=CURRENT_TIMESTAMP'
        'WHERE id=?'
        ( total_food_quantity, temperature, required_temperature, cage_id, mode)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, total_food_quantity, temperature, required_temperature, mode'
        ' FROM cage'
        ' WHERE id=?',
        (cage_id,)
    ).fetchone()
    return jsonify({
        'status': 'Cage successfully updated',
        'data': {
            'id': check['id'],
            'timesamp': check['timestamp'],
            'total_food_quantity': check['total_food_quantity'],
            'temperature' : check['temperature'],
            'required_temperature' : check['required_temperature'],
            'mode' : check['mode']
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