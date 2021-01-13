import sqlite3


def sql_query(query):
    with sqlite3.connect("users.db") as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
        except sqlite3.Error:
            pass
        result = cursor.fetchall()
        return result


def create_tables():
    users_query = "CREATE TABLE IF NOT EXISTS users (user_id INTEGER, channel TEXT)"
    sql_query(users_query)


def add_channel(user, channel):
    try:
        check_query = (
            f"SELECT * FROM users WHERE user_id={user} AND channel='{channel}'"
        )
        check_data = sql_query(check_query)
        if check_data:
            return "The channel already exists in repost list."
        insert_to_db_query = f"INSERT INTO users VALUES({user}, '{channel}')"
        sql_query(insert_to_db_query)
        return "Done! You can write next name of channel"
    except sqlite3.Error:
        return "Error"


def delete_channel(user, channel):
    try:
        check_query = (
            f"SELECT * FROM users WHERE user_id={user} AND channel='{channel}'"
        )
        check_data = sql_query(check_query)
        if not check_data:
            return "The channel does not exist in the list."
        del_from_db_query = (
            f"DELETE FROM users WHERE user_id={user} AND channel='{channel}'"
        )
        sql_query(del_from_db_query)
        return "Channel is deleted from the list!\nYou can write next name of channel."
    except sqlite3.Error:
        return "Error"


create_tables()
