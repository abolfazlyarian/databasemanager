from kubernetes import client, config, watch
import logging
import postgres_management as pm
import os

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] --> %(message)s \n'
)
logging.info("---------------------- Running ------------------")

# load Kubernetes configuration from default location
config.load_incluster_config()

# create a Kubernetes API client
api_instance = client.AppsV1Api()

# define the namespace
namespace = os.environ.get('namespace', default='default')

# watch for events in the specified namespace
stream = watch.Watch()

# iterate through events
for event in stream.stream(api_instance.list_namespaced_deployment, namespace):
    # check the event is the type of 'ADDED' 
    if event['type'] in ['ADDED']:
        # extract annotations from metadata
        deployment = event['object']
        annotations = deployment.metadata.annotations

        # check the required annotations exist
        db_name = annotations.get('postgresql.db')
        db_user = annotations.get('postgresql.user')
        
        if db_name is not None and db_user is not None:
            logging.info("db_name: %s", db_name)
            logging.info("db_user: %s", db_user)

            # connect to database as superuser
            try:
                conn = pm.psql_connection(
                                            db_name='postgres',
                                            db_user='postgres',
                                            db_pass='postgres',
                                            host='postgresql-headless.default.svc.cluster.local'
                                         )
            except Exception as e:
                logging.error("Failed to connect to the database: %s", str(e))

            # create database
            cursor = conn.cursor()
            db_pass = os.environ.get('DB_PASS', default='12345')
            pm.create_database(cursor, db_name=db_name, db_user=db_user, db_pass=db_pass)
            conn.close()
            
            # check the databases is created or not
            try:
                conn = pm.psql_connection(
                                            db_name=db_name,
                                            db_user=db_user,
                                            db_pass='12345',
                                            host='postgresql-headless.default.svc.cluster.local'
                                         )
                conn.close()
                logging.info("The %s database for the %s user has been created successfully", db_name, db_user)
            except:
                logging.info("The %s database for the %s user has not been created successfully", db_name, db_user)
        
        else:
            logging.info("Annotations 'postgresql.db' or 'postgresql.user' are missing or None.")
