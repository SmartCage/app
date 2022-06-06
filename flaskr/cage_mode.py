from flask import request
from flask_restful import Resource
from db import get_db

cage_types = [ 'petShop', 'personal']

modes_preferences = {cage_types[0] :
    "UPDATE light "
    "SET intensity = 2 "
    "WHERE id=?",
    cage_types[1] :
    "UPDATE light "
    "SET intensity = 2 "
    "WHERE id=?", 
}

class cageMode(Resource):
    def get(self, id):
        cageMode = get_db().execute(
            'SELECT mode '
            'FROM cage '
            'WHERE id=?', (str(id),)
            ).fetchone()
        if cageMode is None:
            return {'Status': 'Invalid cage id'}, 403
        else:
            return {'cage mode': str(cageMode['mode'])}, 200


    def put(self, id):
        type = request.args.getlist('type')[0]

        db = get_db()
        cage_id = get_db().execute(
            'SELECT id '
            'FROM cage '
            'WHERE id=?', (str(id),)
            ).fetchone()

        if type not in cage_types:
            return {'Status' : 'Undentified type'}, 403
        if cage_id is None:
            return {'Status' : 'No cage with this id'}, 403

        db.execute(
            'UPDATE cage '
            'SET mode=? '
            'WHERE id=?', (type, str(id))
            )

        db.commit()

        light_id = db.execute(
            "SELECT id, timestamp "
            "FROM light "
            "WHERE cage_id=? "
            "ORDER BY timestamp DESC "
            ,(str(id), )
            ).fetchone()

        db.execute(modes_preferences[type], (light_id['id'],))
        db.commit()

        return {'Status': 'cage mode changed successfully'}, 200
