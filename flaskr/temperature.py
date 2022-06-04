from db import get_db


def set_temperature():
    cages = get_db().execute(
        'SELECT id'
        ' FROM cage'
    ).fetchall()

    mesg = ""

    if cages is not None:
        for c in cages:
            new_temp = get_db().execute(
                'SELECT required_temperature'
                'WHERE id=?',
                str(c['id'])
            ).fetchall()


            get_db().execute(
                'UPDATE temperature'
                'SET temperature=?, timestamp=CURRENT_TIMESTAMP'
                'WHERE id=?',
                (new_temp, str(c['id']))
            )
            get_db().commit()


            mesg += f"--cage {c['id']} " \
                    f"temperature was examined and set to {new_temp}.-- "

    return {
        'temperature check': mesg
    }

        