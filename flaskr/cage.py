from db import get_db
from flask import (Blueprint, jsonify, request)


bp = Blueprint("cage", __name__)

@bp.route("/cage", methods=["GET"])
def get_cage():
    all_cages = get_db().execute(
        'SELECT id, timestamp, default_mode, total_food_quantity'
        ' FROM cage'
        ' ORDER BY timestamp DESC'
    ).fetchall()
    result = ""
    for row in all_cages:
        result = result + str(row['id']) + " " + str(row['default_mode']) + " " + str(row['total_food_quantity']) \
                 + " " + str(row['timestamp']) + "\n"
    return result

@bp.route("/cage", methods=["POST"])
def set_cage():
    default_mode = request.form["mode"]
    total_quantity = request.form["total_quant"]
    

    if not default_mode:
        return jsonify({'status': 'Please enter desired mode'}), 403
    elif not total_quantity:
        return jsonify({'status': 'Please enter total quantity'}), 403

    print(default_mode)
    print(total_quantity)
    db = get_db()
    db.execute(
        'INSERT INTO cage(default_mode, total_food_quantity)'
        ' VALUES (?, ?)',
        (default_mode, total_quantity)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, default_mode, total_food_quantity'
        ' FROM cage'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Success',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'default_mode': check['default_mode'],
            'total_food_quantity': check['total_food_quantity']
        }
    }), 200

@bp.route("/cage", methods=["PUT"])
def update_cage():
    cage_id = request.form["id"]
    default_mode = request.form["mode"]
    total_food_quantity = request.form["total_quant"]

    if not cage_id:
        return jsonify({'status': 'Please enter cage id'}), 403
    elif not total_food_quantity:
        return jsonify({'status': 'Please enter food quantity'}), 403
    elif not default_mode:
        return jsonify({'status': 'Please enter default mode'}), 403

    print(cage_id)
    print(total_food_quantity)
    print(default_mode)

    db = get_db()
    db.execute(
        'UPDATE cage'
        ' SET default_mode=?, total_food_quantity=?, timestamp=CURRENT_TIMESTAMP'
        ' WHERE id=?',
        (default_mode, total_food_quantity, cage_id)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, default_mode, total_food_quantity'
        ' FROM cage'
        ' WHERE id=?',
        cage_id
    ).fetchone()
    return jsonify({
        'status': 'Success',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'default_mode': check['default_mode'],
            'total_food_quantity': check['total_food_quantity']
        }
    }), 200


@bp.route("/cage", methods=["DELETE"])
def delete_food():
    cage_id = request.form["id"]

    if not cage_id:
        return jsonify({'status': 'Please enter cage id'}), 403

    print(cage_id)

    db = get_db()
    db.execute(
        'DELETE FROM cage'
        ' WHERE id=?',
        cage_id
    )
    db.commit()

    return jsonify({
        'status': 'Success',
    }), 200