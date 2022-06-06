from flask import (Blueprint, request, jsonify)
from db import get_db


bp = Blueprint("feeding_schedule", __name__)


@bp.route("/feeding_schedule", methods=["GET"])
def get_feeding_schedule():
    all_feeding_schedules = get_db().execute(
        'SELECT * '
        'FROM feeding_schedule '
        'ORDER BY timestamp DESC'
    ).fetchall()

    result = ""
    for i in all_feeding_schedules:
        fields = [str(i["id"]), f"cage={str(i['cage_id'])}", f"food_name={str(i['food_nameid'])}",
                  f"schedule={str(i['schedule'])}", f"available_type_quantity={str(i['available_type_quantity'])}",
                  str(i["timestamp"])]
        result += " ".join(fields)

    return result


@bp.route("/feeding_schedule", methods=["POST"])
def set_feeding_schedule():
    cage_id = request.form["cage_id"]
    food_name_id = request.form["food_name_id"]
    schedule = request.form["schedule"]
    available_type_quantity = request.form["available_type_quantity"]

    if not cage_id:
        return jsonify({"status": "Cage is required."}), 403
    elif not food_name_id:
        return jsonify({"status": "Food type is required."}), 403
    elif not schedule:
        return jsonify({"status": "Schedule is required."}), 403
    elif not available_type_quantity:
        return jsonify({"status": "Available type quantity is required."}), 403

    print(cage_id)
    print(food_name_id)
    print(schedule)
    print(available_type_quantity)

    db = get_db()
    db.execute(
        'INSERT INTO feeding_schedule(cage_id, food_name_id, schedule, available_type_quantity) '
        'VALUES (?, ?, ?, ?)',
        (cage_id, food_name_id, schedule, available_type_quantity)
    )
    db.commit()

    check = get_db().execute(
        'SELECT * '
        'FROM feeding_schedule '
        'ORDER BY timestamp DESC'
    ).fetchone()

    return jsonify({
        "status": "Feeding schedule successfully recorded.",
        "data": {
            "id": check["id"],
            "cage_id": check["cage_id"],
            "food_name_id": check["food_name_id"],
            "schedule": check["schedule"],
            "available_type_quantity": check["available_type_quantity"],
            "timestamp": check["timestamp"]
        }
    }), 200


@bp.route("/feeding_schedule", methods=["PUT"])
def update_feeding_schedule():
    feeding_id = request.form["id"]
    cage_id = request.form["cage_id"]
    food_name_id = request.form["food_name_id"]
    schedule = request.form["schedule"]
    available_type_quantity = request.form["available_type_quantity"]

    if not feeding_id:
        return jsonify({"status": "Feeding schedule id is required."}), 403
    elif not cage_id:
        return jsonify({"status": "Cage is required."}), 403
    elif not food_name_id:
        return jsonify({"status": "Food name is required."}), 403
    elif not schedule:
        return jsonify({"status": "Schedule is required."}), 403
    elif not available_type_quantity:
        return jsonify({"status": "Available type quantity is required."}), 403

    print(feeding_id)
    print(cage_id)
    print(food_name_id)
    print(schedule)
    print(available_type_quantity)

    db = get_db()
    db.execute(
        'UPDATE feeding_schedule '
        'SET cage_id=?, food_name_id=?, schedule=?, available_type_quantity=?, timestamp=CURRENT_TIMESTAMP '
        'WHERE id=?',
        (cage_id, food_name_id, schedule, available_type_quantity, feeding_id)
    )
    db.commit()

    check = get_db().execute(
        'SELECT * '
        'FROM feeding_schedule '
        'WHERE id=?',
        (feeding_id,)
    ).fetchone()

    if not check:
        return jsonify({'status': 'Feeding schedule does not exist.'}), 404

    return jsonify({
        "status": "Feeding schedule successfully updated",
        "data": {
            "id": check["id"],
            "cage_id": check["cage_id"],
            "food_name_id": check["food_name_id"],
            "schedule": check["schedule"],
            "available_type_quantity": check["available_type_quantity"],
            "timestamp": check["timestamp"]
        }
    }), 200


@bp.route("/feeding_schedule/<string:_id>", methods=["DELETE"])
def delete_feeding_schedule(_id):
    if not _id:
        return jsonify({"status": "Feeding schedule id is required."}), 403

    print(_id)

    db = get_db()
    db.execute(
        'DELETE FROM feeding_schedule '
        'WHERE id=?',
        (_id,)
    )
    db.commit()

    return jsonify({
        "status": "Feeding schedule successfully deleted"
    }), 200