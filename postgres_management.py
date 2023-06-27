import psycopg2


def psql_connection(db_name="postgres", db_user='postgres', db_pass='1376920', host='127.0.0.1'):

    conn = psycopg2.connect(
    database=db_name, user=db_user, password=db_pass, host=host, port= '5432'
    )
    conn.autocommit = True

    return conn

def create_database(cursor, db_name, db_user, db_pass):
    
    #Creating a database
    sql = f"CREATE DATABASE {db_name};"
    cursor.execute(sql)

    #Creating a user with password  
    sql = f"CREATE USER {db_user} WITH ENCRYPTED PASSWORD '{db_pass}';"
    cursor.execute(sql)

    #Grant
    sql = f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};"
    cursor.execute(sql)

#establishing the connection
# conn = psql_connection()
# #Creating a cursor object using the cursor() method
# cursor = conn.cursor()

# #create a database
# create_database(cursor, db_name='test3', db_user='abolfazl2', db_pass='123456')

#Closing the connection
# conn.close()