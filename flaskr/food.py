from flask import (Blueprint, request, jsonify)

from db import get_db

bp = Blueprint('food', __name__)


@bp.route('/food', methods=['GET'])
def get_food():
    all_foods = get_db().execute(
        'SELECT id, timestamp, name, quantity'
        ' FROM food'
        ' ORDER BY timestamp DESC'
    ).fetchall()
    result = ""
    for row in all_foods:
        result = result + str(row['id']) + " " + str(row['name']) + " " + str(row['quantity'])\
                 + " " + str(row['timestamp']) + "\n"
    return result


@bp.route('/food', methods=['POST'])
def set_food():
    food_name = request.form['food']
    quantity = request.form['quant']

    if not food_name:
        return jsonify({'status': 'Please enter the food name.'}), 403
    elif not quantity:
        return jsonify({'status': 'Please enter the food quantity.'}), 403
    print(food_name)
    print(quantity)
    db = get_db()
    db.execute(
        'INSERT INTO food (name, quantity)'
        ' VALUES (?, ?)',
        (food_name, quantity)
    )
    db.commit()
    check = get_db().execute(
        'SELECT id, timestamp, name, quantity'
        ' FROM food'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Success',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'name': check['name'],
            'quantity': check['quantity']
         }
         }), 200

@bp.route('/food', methods=['DELETE'])
def delete_food():
    food_id = request.form['id']

    if not food_id:
        return jsonify({'status': 'Please enter a food name '}), 403

    print(food_id)

    db = get_db()
    db.execute(
        'DELETE FROM food'
        ' WHERE id=?',
        food_id
    )
    db.commit()

    return jsonify({
        'status': 'Success',
    }), 200 


@bp.route('/food', methods=['PUT'])
def update_food():
    food_id = request.form['id']
    food_name = request.form['food']
    quantity = request.form['quant']

    if not food_id:
        return jsonify({'status': 'Please enter a food id '}), 403
    elif not quantity:
        return jsonify({'status': 'Please enter food quantity '}), 403
    elif not food_name:
        return jsonify({'status': 'Please enter the food name'}), 403

    print(food_id)
    print(quantity)
    print(food_name)

    db = get_db()
    db.execute(
        'UPDATE food'
        ' SET name=?, quantity=?, timestamp=CURRENT_TIMESTAMP'
        ' WHERE id=?',
        (food_name, quantity, food_id)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, name, quantity'
        ' FROM food'
        ' WHERE id=?',
        food_id
    ).fetchone()
    return jsonify({
        'status': 'Success',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'name': check['name'],
            'quantity': check['quantity']
        }
    }), 200