import psycopg2


def psql_connection(db_name="postgres", db_user='postgres', db_pass='postgres', host='127.0.0.1'):

    conn = psycopg2.connect(
                            database=db_name,
                            user=db_user, 
                            password=db_pass, 
                            host=host, 
                            port= '5432')
    conn.autocommit = True

    return conn

def create_database(cursor, db_name, db_user, db_pass):
    
    #Creating a database
    sql = f"CREATE DATABASE {db_name};"
    cursor.execute(sql)

    #Creating a user with password  
    sql = f"CREATE USER {db_user} WITH ENCRYPTED PASSWORD '{db_pass}';"
    cursor.execute(sql)

    # Grant
    sql = f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};"
    cursor.execute(sql)
