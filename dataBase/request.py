import psycopg2
import re

from config import user, password, host, db_name

async def insert_data(name_user, surname, tg_id, chat_id):
    try:
        connection=psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        connection.autocommit = True

        cursor = connection.cursor()

        query = "SELECT EXISTS(SELECT 1 FROM users WHERE tg_id=%s)"
        cursor.execute(query, (str(tg_id),))
        exists = cursor.fetchone()[0]

        if str(exists) == 'True':
            pass
        else:
            query = f"INSERT INTO users (name_user, surname, tg_id, chat_id) VALUES ('{name_user}', '{surname}', '{tg_id}', '{chat_id}')"
            cursor.execute(query)

            query1 = f"SELECT id FROM users WHERE tg_id = '{tg_id}'"
            cursor.execute(query1, (str(tg_id),))
            exists1 = cursor.fetchone()[0]

            query4 = f"INSERT INTO admin_tg (user_id, admin_status) VALUES ('{exists1}', 'False')"
            cursor.execute(query4)


        if str(tg_id) == '560824838':
            query2 = f"SELECT (id) FROM users WHERE (tg_id = '560824838')"
            cursor.execute(query2)
            may_id = cursor.fetchone()[0]

            query3 = f"UPDATE admin_tg SET admin_status = 'True' WHERE user_id = %s"
            cursor.execute(query3, (str(may_id),))

    except Exception as ex:
        print(ex)
    finally:
        if connection:
            cursor.close()
            connection.close()

async def show_all():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        connection.autocommit =True
        cursor = connection.cursor()

        query = "SELECT * FROM users;"
        cursor.execute(query)

        rows = cursor.fetchall()

        return rows

    except Exception as ex:
        print(ex)
    finally:
        if connection:
            cursor.close()
            connection.close()

async def check_user(tg_id):
    try:
        connection=psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        connection.autocommit = True

        cursor = connection.cursor()

        query = "SELECT EXISTS(SELECT 1 FROM users WHERE tg_id=%s)"
        cursor.execute(query, (str(tg_id),))
        exists = cursor.fetchone()[0]
        return exists


    except Exception as ex:
        print(ex)
    finally:
        if connection:
            cursor.close()
            connection.close()


async def get_tg_id(id):
    try:
        connection=psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        connection.autocommit = True

        cursor = connection.cursor()

        query = f"SELECT (tg_id) FROM users WHERE (id = '{id}')"
        cursor.execute(query, (int(id),))

        tg_id1 = cursor.fetchone()
        tg_id = re.search(r'\d+', str(tg_id1))
        return tg_id.group(0)
    except Exception as ex:
        print(ex)
    finally:
        if connection:
            cursor.close()
            connection.close()

async def show_all_admin():
    try:
        connection=psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        connection.autocommit = True

        cursor = connection.cursor()

        query = ("SELECT * "
                 "FROM users "
                 "JOIN admin_tg ON users.id = admin_tg.user_id "
                 "WHERE admin_tg.admin_status = True;")
        cursor.execute(query)

        rows = cursor.fetchall()

        # print(rows)

        return rows

    except Exception as ex:
        print(ex)
    finally:
        if connection:
            cursor.close()
            connection.close()

async def insert_admin(tg_id):
    try:
        connection=psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        connection.autocommit = True

        cursor = connection.cursor()

        query1 = f"SELECT id FROM users WHERE tg_id = %s"
        cursor.execute(query1, (tg_id,))
        id = cursor.fetchone()[0]

        # print(id)



        query = "SELECT admin_status FROM admin_tg WHERE user_id=%s"
        cursor.execute(query, (id,))
        exists = cursor.fetchone()[0]

        if exists == 'True':
            pass
        else:
            query2 = f"UPDATE admin_tg SET admin_status = 'True' WHERE user_id = '{id}'"
            cursor.execute(query2, (id,))

        return id

    except Exception as ex:
        print(ex)
    finally:
        if connection:
            cursor.close()
            connection.close()


async def check_admin(tg_id):
    try:
        connection=psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        connection.autocommit = True

        cursor = connection.cursor()

        tg_id = str(tg_id)

        query = f"SELECT id FROM users WHERE tg_id = %s"
        cursor.execute(query, (tg_id,))
        id = str(cursor.fetchall()[0])

        # print(id)
        res = re.search(r'\((\d+)\,\)', id).group(1)
        # print(res)

        query1 = f"SELECT admin_status FROM admin_tg WHERE user_id = %s"
        cursor.execute(query1, (res,))
        flag = str(cursor.fetchall()[0])
        return re.search(r'\((\w+)\,\)', str(flag)).group(1)

    except Exception as ex:
        print(ex)
    finally:
        if connection:
            cursor.close()
            connection.close()

async def get_chat_id(id):
    try:
        connection=psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        connection.autocommit = True

        cursor = connection.cursor()

        query = f"SELECT (chat_id) FROM users WHERE (id = '{id}')"
        cursor.execute(query, (int(id),))
        chat_id = str(cursor.fetchone()[0])

        return chat_id
    except Exception as ex:
        print(ex)
    finally:
        if connection:
            cursor.close()
            connection.close()


async def show_all_children():
    try:
        connection=psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        connection.autocommit = True

        cursor = connection.cursor()

        query = f"SELECT user_id FROM admin_tg WHERE admin_status = 'false'"
        cursor.execute(query)
        id = str(cursor.fetchone()[0])

        query2 = f"SELECT * FROM users WHERE id = '{id}'"
        cursor.execute(query2, int(id))
        fio = cursor.fetchall()
        print(fio)
        return fio
    except Exception as ex:
        print(ex)
    finally:
        if connection:
            cursor.close()
            connection.close()