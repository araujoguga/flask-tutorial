import mysql.connector
cnx = mysql.connector.connect(
    user='dev', database='flaskr', password='root')


def get_cursor():
    return cnx.cursor(dictionary=True)


def close_cursor(cursor):
    cursor.close()


def commit():
    cnx.commit()
