import pymysql.cursors
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='quiz_server',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)


def query(sql, values=""):
    with connection.cursor() as cursor:
        if values != "":
            cursor.execute(sql, values)
            result = cursor.fetchall()
        else:
            cursor.execute(sql)
            result = cursor.fetchall()
    connection.commit()
    return result