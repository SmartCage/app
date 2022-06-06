from db import get_db
from datetime import datetime


def feed_the_parrot():
    current_time = datetime.now()
    current_hour = current_time.strftime("%H:00")

    mesg= ""

    feeding_schedules = get_db().execute(
        'SELECT id, food_name_id, cage_id, schedule, available_type_quantity'
        ' FROM feeding_schedule'
    ).fetchall()

    if feeding_schedules is not None:
        for fs in feeding_schedules:
            hours = str(fs['schedule']).split(';')
            food_tid = fs['food_name_id']
            fs_id = fs['id']
            cage_id = fs['cage_id']
            if current_hour in hours:
                food_to_be_released = get_db().execute(
                    'SELECT name, quantity'
                    ' FROM FOOD'
                    f" WHERE id={food_tid}"
                ).fetchone()
                if fs['available_type_quantity'] >= food_to_be_released['quantity']:
                    mesg+= f"Feeding parrot in cage {fs['cage_id']}" \
                                             f"with name {food_to_be_released['name']}"
                    db = get_db()
                    db.execute(
                        'UPDATE feeding_schedule'
                        f" SET available_type_quantity={fs['available_type_quantity'] - food_to_be_released['quantity']}"
                        f" WHERE id={fs_id}"
                    )
                    db.commit()

                    db = get_db()
                    db.execute(
                        'UPDATE cage'
                        f" SET total_food_quantity=total_food_quantity - { food_to_be_released['quantity']}"
                        f" WHERE id = {cage_id}"
                    )
                    db.commit()
                else:
                    mesg+= f" In cage {fs['cage_id']}" \
                           f"there is no {food_to_be_released['name']}"

    if mesg== "":
        mesg= "All parrot are fed!"
    return {
        'feeding check': mesg
    }

