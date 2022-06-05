from flask import (Blueprint, request, jsonify)

from db import get_db

bp = Blueprint('parrot', __name__)


@bp.route('/parrot', methods=['GET'])
def get_parrot():
    all_parrot = get_db().execute(
        'SELECT *'
        ' FROM parrot'
        ' ORDER BY timestamp DESC'
    ).fetchall()
    result = ""
    for row in all_parrot:
        result = result + str(row['id']) + " " + str(row['type_id']) + " " \
        + str(row['cage_id']) + " " + str(row['name']) + " " + str(row['health']) \
        + " " + str(row['birthday']) + " " + str(row['timestamp']) + "\n"
    return result


@bp.route('/parrot', methods=['POST'])
def set_parrot():
    name = request.form['name']
    health = request.form['health']
    birthday = request.form['birthday']
    type_id = request.form['type_id']
    cage_id = request.form['cage_id']

    if not name:
        return jsonify({'status': 'Please enter parrot name'}), 403
    elif not health:
        return jsonify({'status': 'Please enter parrot health info '}), 403
    elif not birthday:
        return jsonify({'status': 'Please enter parrot birthday'}), 403
    elif not type_id:
        return jsonify({'status': 'Please enter  parrot type '}), 403
    elif not cage_id:
        return jsonify({'status': 'Please enter  parrot cage '}), 403

    print(f"name is {name}")
    print(f"health is {health}")
    print(f"birthday is {birthday}")
    print(f"parrot type id is {type_id}")
    print(f"cage id is {cage_id}")

    db = get_db()
    db.execute(
        'INSERT INTO parrot (type_id, cage_id, name, health, birthday)'
        ' VALUES (?, ?, ?, ?, ?)',
        (type_id, cage_id, name, health, birthday)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, type_id, cage_id, name, health, birthday, timestamp'
        ' FROM parrot'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Parrot successfully created',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'type_id': check['type_id'],
            'cage_id': check['cage_id'],
            'name': check['name'],
            'health': check['health'],
            'birthday': check['birthday']
        }
    }), 200


@bp.route('/parrot', methods=['PUT'])
def update_parrot():
    parrot_id = request.form['id']
    type_id = request.form['type_id']
    cage_id = request.form['cage_id']
    name = request.form['name']
    health = request.form['health']
    birthday = request.form['birthday']

    if not parrot_id:
        return jsonify({'status': 'Please enter parrot id '}), 403
    elif not type_id:
        return jsonify({'status': 'Please enter parrot type id '}), 403
    elif not cage_id:
        return jsonify({'status': 'Please enter cage id '}), 403
    elif not name:
        return jsonify({'status': 'Please enter parrot name'}), 403
    elif not health:
        return jsonify({'status': 'Please enter parrot health '}), 403
    elif not birthday:
        return jsonify({'status': 'Please enter parrot birthday '}), 403

    print(f"parrot id is {parrot_id}")
    print(f"parrot type id is {type_id}")
    print(f"cage id is {cage_id}")
    print(f"parrot name is {name}")
    print(f"parrot health is {health}")
    print(f"Birthday is {birthday}")

    db = get_db()
    db.execute(
        'UPDATE parrot'
        ' SET type_id=?, cage_id=?, name=?, health=?, birthday=?, timestamp=CURRENT_TIMESTAMP'
        ' WHERE id=?',
        (type_id, cage_id, name, health, birthday, parrot_id)
    )
    db.commit()

    check = get_db().execute(
        'SELECT *'
        ' FROM parrot'
        ' WHERE id=?',
        (parrot_id,)
    ).fetchone()

    if not check:
        return jsonify({'status': 'Parrot not found'}), 404
    return jsonify({
        'status': 'Parrot successfully updated',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'type_id': check['type_id'],
            'cage_id': check['cage_id'],
            'name': check['name'],
            'health': check['health'],
            'birthday': check['birthday']
        }
    }), 200


@bp.route('/parrot/<string:_id>', methods=['DELETE'])
def delete_parrot(_id):
    if not _id:
        return jsonify({'status': 'parrot id is required.'}), 403
    print(f"parrot id is {_id}")

    db = get_db()
    db.execute(
        'DELETE FROM parrot'
        ' WHERE id=?',
        (_id,)
    )
    db.commit()
    return jsonify({'status': 'parrot successfully deleted.'}), 200