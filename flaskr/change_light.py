from flask import request
from flask_restful import Resource
from db import get_db


def is_cage_id_valid(id):
    db = get_db()
    cageMode = get_db().execute(
        'SELECT id '
        'FROM cage '
        'WHERE id=?', (id,)
        ).fetchone()
    if cageMode is None:
        return False
    else:
        return True


class LightIntensity(Resource):
    def get(self, cage_id):
        db = get_db()
        if is_cage_id_valid(cage_id) == False:
            return {'Status': 'Invalid cage id!'}, 403

        light_data = db.execute(
            "SELECT intensity "
            "FROM light "
            "WHERE cage_id=? "
            "ORDER BY timestamp DESC "
            ,(str(cage_id), )
            ).fetchone()

        return {'Light intensity': light_data['intensity']}, 200


    def put(self, cage_id):
        db = get_db()
        intensity = request.args.getlist('intensity')[0]

        if is_cage_id_valid(cage_id) is False:
            return {'Status': 'Invalid cage id!'}, 403

        print ('cage id exist? :' + str(cage_id))

        light_data = db.execute(
            "SELECT intensity, id "
            "FROM light "
            "WHERE cage_id=? "
            "ORDER BY timestamp DESC "
            ,(cage_id, )
            ).fetchone()

        db.execute(
            "UPDATE light "
            "SET intensity=? "
            "WHERE id=?", (intensity, light_data['id']))

        db.commit()

        return {'Status': 'Intensity was set successfully '}, 200
