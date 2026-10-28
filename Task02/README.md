# Лабораторная работа 2. Создание и заполнение базы данных movies_rating.db

## Требования к окружению
- Python 3
- SQLite (утилита `sqlite3` должна быть доступна в PATH)
- Bash: Linux, macOS или Git Bash в Windows

## Файлы
- `movies.csv`, `ratings.csv`, `tags.csv`, `users.txt`, `genres.txt`, `occupation.txt` — исходные данные.
- `make_db_init.py` — утилита, генерирующая SQL-скрипт `db_init.sql`.
- `db_init.bat` — shell-скрипт, который запускает утилиту и загружает результат в базу.

## Запуск
```bash
./db_init.bat
```
Если файл не запускается как исполняемый: `bash db_init.bat`.

## Результат
После выполнения создаётся файл `db_init.sql` и база данных `movies_rating.db` с таблицами `movies`, `ratings`, `tags`, `users`. Если таблицы в базе уже есть, они удаляются и создаются заново.

## Структура таблиц
- `movies`: id, title, year, genres. Год выделяется из названия фильма; если года нет, значение NULL.
- `ratings`: id, user_id, movie_id, rating, timestamp.
- `tags`: id, user_id, movie_id, tag, timestamp.
- `users`: id, name, email, gender, register_date, occupation.