import csv
import re
from pathlib import Path

# Папка, в которой лежит скрипт и исходные данные
BASE = Path(__file__).resolve().parent
OUT = BASE / "db_init.sql"

# "Toy Story (1995)" -> название и год
YEAR_RE = re.compile(r"^(.*?)\s*\((\d{4})\)\s*$")

SCHEMA = """
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS users;

CREATE TABLE movies (
    id     INTEGER PRIMARY KEY,
    title  VARCHAR(200) NOT NULL,
    year   INTEGER,
    genres VARCHAR(100)
);
CREATE TABLE ratings (
    id        INTEGER PRIMARY KEY,
    user_id   INTEGER NOT NULL,
    movie_id  INTEGER NOT NULL,
    rating    REAL NOT NULL,
    timestamp INTEGER NOT NULL
);
CREATE TABLE tags (
    id        INTEGER PRIMARY KEY,
    user_id   INTEGER NOT NULL,
    movie_id  INTEGER NOT NULL,
    tag       VARCHAR(100) NOT NULL,
    timestamp INTEGER NOT NULL
);
CREATE TABLE users (
    id            INTEGER PRIMARY KEY,
    name          VARCHAR(50) NOT NULL,
    email         VARCHAR(50),
    gender        VARCHAR(10),
    register_date VARCHAR(10),
    occupation    VARCHAR(30)
);
"""


def q(value):
    """Строка в кавычках для SQL: апостроф удваивается."""
    return "'" + value.replace("'", "''") + "'"


def read_csv(name):
    with open(BASE / name, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        next(reader)  # пропускаем заголовок
        return list(reader)


def read_users(name):
    with open(BASE / name, encoding="utf-8-sig") as f:
        return [line.rstrip("\r\n").split("|") for line in f if line.strip()]


def main():
    lines = [SCHEMA, "BEGIN TRANSACTION;"]

    movies = read_csv("movies.csv")
    for movie_id, title, genres in movies:
        m = YEAR_RE.match(title)
        if m:
            title, year = m.group(1), m.group(2)
        else:
            year = "NULL"
        lines.append(
            f"INSERT INTO movies (id, title, year, genres) "
            f"VALUES ({int(movie_id)}, {q(title.strip())}, {year}, {q(genres)});"
        )

    ratings = read_csv("ratings.csv")
    for i, (user_id, movie_id, rating, ts) in enumerate(ratings, start=1):
        lines.append(
            f"INSERT INTO ratings (id, user_id, movie_id, rating, timestamp) "
            f"VALUES ({i}, {int(user_id)}, {int(movie_id)}, {float(rating)}, {int(ts)});"
        )

    tags = read_csv("tags.csv")
    for i, (user_id, movie_id, tag, ts) in enumerate(tags, start=1):
        lines.append(
            f"INSERT INTO tags (id, user_id, movie_id, tag, timestamp) "
            f"VALUES ({i}, {int(user_id)}, {int(movie_id)}, {q(tag)}, {int(ts)});"
        )

    users = read_users("users.txt")
    for user_id, name, email, gender, reg_date, occupation in users:
        lines.append(
            f"INSERT INTO users (id, name, email, gender, register_date, occupation) "
            f"VALUES ({int(user_id)}, {q(name)}, {q(email)}, {q(gender)}, "
            f"{q(reg_date)}, {q(occupation)});"
        )

    lines.append("COMMIT;")

    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    print(f"movies: {len(movies)}, ratings: {len(ratings)}, "
          f"tags: {len(tags)}, users: {len(users)}")


if __name__ == "__main__":
    main()