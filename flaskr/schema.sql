DROP TABLE IF EXISTS cage;
DROP TABLE IF EXISTS facility;
DROP TABLE IF EXISTS feeding_schedule;
DROP TABLE IF EXISTS food;
DROP TABLE IF EXISTS light;
DROP TABLE IF EXISTS parrot;
DROP TABLE IF EXISTS parrot_type;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS heat;


CREATE TABLE cage(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  temperature REAL NOT NULL,
  required_temperature REAL NOT NULL,
  total_food_quantity REAL NOT NULL,
  mode TEXT NOT NULL,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE facility (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cage_id INTEGER NOT NULL,
  electricity INTEGER NOT NULL,
  movement_sensor INTEGER NOT NULL,
  temperature_sensor INTEGER NOT NULL,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (cage_id) REFERENCES cage (id)
);

CREATE TABLE food (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name_food TEXT NOT NULL,
  quantity REAL NOT NULL,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE light (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cage_id INTEGER NOT NULL,
  intensity REAL NOT NULL,
  start_light TEXT NOT NULL,
  end_light TEXT NOT NULL,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (cage_id) REFERENCES cage (id)
);


CREATE TABLE heat (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cage_id INTEGER NOT NULL,
  intensity REAL NOT NULL,
  max_heat TEXT NOT NULL,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (cage_id) REFERENCES cage (id)
);

CREATE TABLE feeding_schedule (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cage_id INTEGER NOT NULL,
  food_name_id INTEGER NOT NULL,
  schedule TEXT NOT NULL,
  available_type_quantity REAL NOT NULL,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (cage_id) REFERENCES cage (id),
  FOREIGN KEY (food_name_id) REFERENCES food (id)
);



CREATE TABLE parrot_type (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  food_id INTEGER NOT NULL,
  min_light_intensity REAL NOT NULL,
  max_light_intensity REAL NOT NULL,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (food_id) REFERENCES food (id)
);


CREATE TABLE parrot (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type_id INTEGER NOT NULL,
  cage_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  health INTEGER NOT NULL,
  birthday TEXT,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (cage_id) REFERENCES cage (id),
  FOREIGN KEY (type_id) REFERENCES parrot_type (id)
);


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);



CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);