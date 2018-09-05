import pymysql.cursors

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='quiz_server',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)


def query(sql, values=None):
    """
    Generic query that returns all data. 
    """
    with connection.cursor() as cursor:
        if values:
            cursor.execute(sql, values)
            result = cursor.fetchall()
        else:
            cursor.execute(sql)
            result = cursor.fetchall()
    connection.commit()
    return result


def insert_many(sql, values):
    """
    Used to insert many values
    """
    with connection.cursor() as cursor:
        cursor.executemany(sql, values)
    connection.commit()


def insert_query(sql, values=None):
    """
    Used to insert one row
    """
    with connection.cursor() as cursor:
        if values:
            cursor.execute(sql, values)
            result = cursor.lastrowid
        else:
            cursor.execute(sql)
            result = cursor.lastrowid
    connection.commit()
    return result


def query_rowcount(sql, values=None):
    """
    Used if you want to see how many rows were effects e.g. (DELETE, UPDATE)
    """
    with connection.cursor() as cursor:
        if values:
            cursor.execute(sql, values)
            result = cursor.rowcount
        else:
            cursor.execute(sql)
            result = cursor.rowcount
    connection.commit()
    return result
