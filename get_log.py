import sqlite3


def print_data():
    conn_log = sqlite3.connect('logs.db', check_same_thread=False)
    log = conn_log.execute(f"SELECT * FROM logs").fetchall()
    for i in log:
        print(i)


if __name__ == '__main__':
    print_data()
