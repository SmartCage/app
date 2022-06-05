import csv

from app import create_app
from db import get_db


def add_cages(cages_path):
    file = open(cages_path)
    content = csv.reader(file, delimiter=',')
    index = 1
    for line in content:
        if index > 0:
            total_food_quantity, temperature, required_temperature = line
            database = get_db()
            database.execute(
                "INSERT INTO cage( temperature, required_temperature,total_food_quantity) "
                "VALUES (?, ?, ?, ?)",
                ( temperature, required_temperature, total_food_quantity)
            )
            database.commit()
        index += 1




def add_food(food_path):
    file = open(food_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            food_name, quantity = line
            database = get_db()
            database.execute(
                "INSERT INTO food(name, quantity) "
                "VALUES (?, ?)",
                (food_name, quantity)
            )
            database.commit()
        index += 1


def add_feeding_schedules(feeding_schedules_path):
    file = open(feeding_schedules_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            schedule, available_type_quantity, cage_id, food_name_id = line

            database = get_db()

           

            database.execute(
                "INSERT INTO feeding_schedule(schedule, available_type_quantity, cage_id, food_name_id) "
                "VALUES (?, ?, ?, ?)",
                (schedule, available_type_quantity, cage_id, food_name_id)
            )
            database.commit()
        index += 1


def add_parrot_types(parrot_types_path):
    file = open(parrot_types_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            name, food_id, min_light_intensity, max_light_intensity = line

            database = get_db()

            database.execute(
                "INSERT INTO parrot_type(name, food_id, min_light_intensity, "
                "max_light_intensity) "
                "VALUES (?, ?, ?, ?)",
                (name, food_id,  min_light_intensity, max_light_intensity)
            )
            database.commit()
        index += 1


def add_parrot(parrot_path):
    file = open(parrot_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            type_id, cage_id,name,  health, birthday = line

            database = get_db()

            database.execute(
                "INSERT INTO parrot( type_id, cage_id,name,health,birthday) "
                "VALUES (?, ?, ?, ?, ?)",
                ( type_id, cage_id,name, health, birthday)
            )
            database.commit()
        index += 1


def add_light(light_path):
    file = open(light_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            cage_id, intensity, start, end = line

            database = get_db()

            cage = database.execute(
                "SELECT id "
                "FROM cage "
                "WHERE id=?",
                (cage_id,)
            ).fetchone()
            cage_id = cage["id"]

            database.execute(
                "INSERT INTO light(cage_id, intensity, start, end) "
                "VALUES (?, ?, ?, ?)",
                (cage_id, intensity, start, end)
            )
            database.commit()
        index += 1


def add_heat(heat_path):
    file = open(heat_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            cage_id, intensity, max_heat = line

            database = get_db()

            cage = database.execute(
                "SELECT id "
                "FROM cage "
                "WHERE id=?",
                (cage_id,)
            ).fetchone()
            cage_id = cage["id"]

            database.execute(
                "INSERT INTO heat(cage_id, intensity, max_heat) "
                "VALUES (?, ?, ?)",
                (cage_id, intensity, max_heat)
            )
            database.commit()
        index += 1


if __name__ == "__main__":
    local_app = create_app()
    with local_app.app_context():
        add_cages("db-data/cage.csv")
        add_food("./db-data/food.csv")
        add_feeding_schedules("./db-data/feeding_schedule.csv")
        add_parrot_types("./db-data/parrot_type.csv")
        add_parrot("./db-data/parrot.csv")
        add_light("./db-data/light.csv")
        add_heat("./db-data/heat.csv")