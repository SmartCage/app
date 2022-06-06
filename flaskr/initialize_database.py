import csv

from app import create_app
from db import get_db


def add_cages(cages_path):
    file = open(cages_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            temperature, required_temperature, total_food_quantity, mode = line
            database = get_db()
            database.execute(
                "INSERT INTO cage(temperature, required_temperature, total_food_quantity, mode) "
                "VALUES (?, ?, ?, ?)",
                (temperature, required_temperature, total_food_quantity, mode)
            )
            database.commit()
        index += 1


def add_facilities(facilities_path):
    file = open(facilities_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            cage_id, electricity, movement_sensor, temperature_sensor = line

            database = get_db()


            database.execute(
                "INSERT INTO facility(cage_id, electricity, movement_sensor, temperature_sensor) "
                "VALUES (?, ?, ?, ?)",
                (cage_id, electricity, movement_sensor, temperature_sensor)
            )
            database.commit()
        index += 1


def add_food(food_path):
    file = open(food_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            name_food, quantity = line
            database = get_db()
            database.execute(
                "INSERT INTO food(name_food, quantity) "
                "VALUES (?, ?)",
                (name_food, quantity)
            )
            database.commit()
        index += 1


def add_feeding_schedules(feeding_schedules_path):
    file = open(feeding_schedules_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            cage_id, food_name_id, schedule, available_type_quantity = line

            database = get_db()


            database.execute(
                "INSERT INTO feeding_schedule(cage_id, food_name_id, schedule, available_type_quantity) "
                "VALUES (?, ?, ?, ?)",
                (cage_id, food_name_id, schedule, available_type_quantity)
            )
            database.commit()
        index += 1


def add_parrot_types(parrot_types_path):
    file = open(parrot_types_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            name, name_food, min_light_intensity, max_light_intensity = line

            database = get_db()

            food = database.execute(
                "SELECT id "
                "FROM food_food "
                "WHERE name=?",
                (name_food,)
            ).fetchone()
            food_id = food["id"]

            database.execute(
                "INSERT INTO parrot_type(name, food_id, min_light_intensity, max_light_intensity) "
                "VALUES (?, ?, ?, ?)",
                (name, food_id, min_light_intensity, max_light_intensity)
            )
            database.commit()
        index += 1


def add_parrot(parrot_path):
    file = open(parrot_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            parrot_type_name, cage_id, name, health, birthday = line

            database = get_db()

            parrot_type = database.execute(
                "SELECT id "
                "FROM parrot_type "
                "WHERE name=?",
                (parrot_type_name,)
            ).fetchone()
            parrot_type_id = parrot_type["id"]

            database.execute(
                "INSERT INTO parrot(type_id, cage_id, name, health, birthday) "
                "VALUES (?, ?, ?, ?, ?)",
                (parrot_type_id, cage_id, name, health, birthday)
            )
            database.commit()
        index += 1


def add_light(light_path):
    file = open(light_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            cage_id, intensity, schedule = line

            database = get_db()

            database.execute(
                "INSERT INTO light(cage_id, intensity, schedule) "
                "VALUES (?, ?, ?, ?)",
                (cage_id, intensity, schedule)
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


            database.execute(
                "INSERT INTO heat(cage_id, intensity, max_heat) "
                "VALUES(?,  ?)",
                (cage_id,  intensity, max_heat)
            )
            database.commit()
        index += 1


if __name__ == "__main__":
    local_app = create_app()
    with local_app.app_context():
        add_cages("initial_data/cage.csv")
        add_facilities("./initial_data/facility.csv")
        add_food("./initial_data/food.csv")
        add_feeding_schedules("./initial_data/feeding_schedule.csv")
        add_parrot_types("./initial_data/parrot_type.csv")
        add_parrot("./initial_data/parrot.csv")
        add_light("./initial_data/light.csv")
        add_heat("./initial_data/heat.csv")