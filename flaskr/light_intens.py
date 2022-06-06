from db import get_db


def light_intensity():
    cages = get_db().execute(
        'SELECT id'
        ' FROM cage'
    ).fetchall()

    message_queue = ""
    db = get_db()

    if cages is not None:
        for c in cages:

            parrot_types = db.execute(
                'SELECT DISTINCT type_id'
                ' FROM parrot'
                ' WHERE cage_id = ?'
                ' ORDER BY timestamp DESC',
                str(c['id'])
            ).fetchall()

            if parrot_types is not None:
                lowest = [15]
                highest = [25]

                for x in parrot_types:
                    check_val = x['type_id']
                    lowest_possible = db.execute(
                        'SELECT min_light_intensity'
                        ' FROM parrot_type'
                        f' WHERE id={check_val}'
                    ).fetchone()
                    lowest.append(lowest_possible['min_light_intensity'])

                    highest_possible = db.execute(
                        'SELECT max_light_intensity'
                        ' FROM parrot_type'
                        f' WHERE id={check_val}'
                    ).fetchone()
                    highest.append(highest_possible['max_light_intensity'])

                    new_intensity = (max(lowest) + min(highest)) / 2

                    db.execute(
                        'UPDATE light'
                        ' SET intensity=?, timestamp=CURRENT_TIMESTAMP'
                        ' WHERE id=?',
                        (new_intensity, str(c['id']))
                    )

                    db.commit()
                    message_queue += f"--cage {c['id']} " \
                                     f"light intensity was set to {new_intensity}.-- "
    return {
        'light intensity check': message_queue
    }