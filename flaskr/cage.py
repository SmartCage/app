from db import get_db
from flask import (Blueprint, jsonify, request)


bp = Blueprint("cage", __name__)


@bp.route("/cage", methods=["POST"])
def set_cage():
    default_mode = request.form["mode"]
    total_quantity = request.form["total_quant"]
    error = None

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