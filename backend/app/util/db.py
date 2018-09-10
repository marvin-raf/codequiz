import pymysql.cursors
from config import config
from DBUtils.PersistentDB import PersistentDB

dbConn = None


def connect_db():
    return PersistentDB(
        creator=pymysql,  # the rest keyword arguments belong to pymysql
        user='root',
        password='',
        database='quiz_server',
        autocommit=True,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)


def get_db():
    global dbConn
    '''Opens a new database connection per app.'''

    if not dbConn:
        dbConn = connect_db()
    return dbConn.connection()


def query(sql, values=None):
    """
    Generic query that returns all data. 
    """
    global dbConn
    with get_db().cursor() as cursor:
        if values:
            cursor.execute(sql, values)
            result = cursor.fetchall()
        else:
            cursor.execute(sql)
            result = cursor.fetchall()

    return result


def insert_many(sql, values):
    """
    Used to insert many values
    """

    with get_db().cursor() as cursor:
        cursor.executemany(sql, values)


def insert_query(sql, values=None):
    """
    Used to insert one row
    """

    with get_db().cursor() as cursor:
        if values:
            cursor.execute(sql, values)
            result = cursor.lastrowid
        else:
            cursor.execute(sql)
            result = cursor.lastrowid
    return result


def query_rowcount(sql, values=None):
    """
    Used if you want to see how many rows were effects e.g. (DELETE, UPDATE)
    """

    with get_db().cursor() as cursor:
        if values:
            cursor.execute(sql, values)
            result = cursor.rowcount
        else:
            cursor.execute(sql)
            result = cursor.rowcount
    return result
