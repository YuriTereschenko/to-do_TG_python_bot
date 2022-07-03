import sqlite3
import datetime as dt
conn = sqlite3.connect('users_tasks_list.db', check_same_thread=False)
conn_log = sqlite3.connect('logs.db', check_same_thread=False)


def db_logs(user_id, task_id, change):
    conn_log.execute(f"""CREATE TABLE IF NOT EXISTS logs(
       date DATE,
       user_id INT,
       task_id INT,
       change TEXT);
    """)

    date = str(dt.datetime.now())
    conn_log.execute(f"""INSERT INTO logs(date, user_id, task_id, change)
           VALUES('{date}','user_id: {user_id}', 'task_id: {task_id}', '{change}');""")
    conn_log.commit()


def db(user_id):
    # conn = sqlite3.connect('users_tasks_list.db')

    conn.execute(f"""CREATE TABLE IF NOT EXISTS user{str(user_id)}(
       task_num INT NOT NULL PRIMARY KEY,
       task_name TEXT,
       task_description TEXT,
       status TEXT);
    """)
    conn.commit()


def add_info_bd(name, description, user_id):
    if bool(max_id(user_id)):
        new_id = max_id(user_id) + 1
    else:
        new_id = 1
    conn.execute(f"""INSERT INTO user{str(user_id)}(task_num,task_name, task_description, status)
       VALUES({new_id},'{name}', '{description}', 'in progress');""")
    conn.commit()
    db_logs(user_id, new_id, 'task created')


def get_data(user_id):
    return conn.execute(f"SELECT * FROM user{user_id};").fetchall()


def update_status(task_id, user_id):
    conn.execute(f"UPDATE user{user_id} SET status = 'completed' WHERE task_num = {task_id}")
    conn.commit()
    db_logs(user_id, task_id, 'task status changed')


def id_exists(user_id, task_id):
    return bool(conn.execute(f"SELECT * FROM user{user_id} WHERE task_num = {task_id}").fetchall())


def max_id(user_id):
    return conn.execute(f"SELECT max(task_num) FROM user{user_id}").fetchone()[0]


def del_data(task_id, user_id):
    conn.execute(f"DELETE FROM user{user_id} WHERE task_num = {task_id}")
    conn.commit()
    db_logs(user_id, task_id, 'task deleted')

