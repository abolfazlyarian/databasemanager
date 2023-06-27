from kubernetes import client, config, watch
import logging
import postgres_management as pm
# Load Kubernetes configuration from default location
logging.basicConfig(
    level=logging.INFO,
)
#config.load_kube_config(config_file="/home/user01/.kube/config")
config.load_incluster_config()

# Create a Kubernetes API client
api_instance = client.AppsV1Api()

# Define the namespace and resource type to watch
namespace = 'yarian'

# Watch for events in the specified namespace and resource type
stream = watch.Watch()

# Iterate through events
logging.info("---------------------- Running ------------------")
for event in stream.stream(api_instance.list_namespaced_deployment, namespace):
    # print("---------------------- Running ------------------")
    # Check if the event is of type 'ADDED' or 'MODIFIED'
    # print(f"------------------------ Event {i} ------------------------")
    # print(event)
    if event['type'] in ['ADDED']: # = MODIFIED
        deployment = event['object']
        # print(f"------------------------ deployment {i} ------------------------")
        # print(deployment)
        # Extract annotations from metadata
        annotations = deployment.metadata.annotations
        # print(f"------------------------ annotation {i} ------------------------")
        # print(annotations)

        # Check if the required annotations exist
        db_name = annotations.get('postgresql.db')
        db_user = annotations.get('postgresql.user')
        
        if db_name is not None and db_user is not None:
            # The annotations exist and are not None
            # Process the db_name and db_user variables here
            logging.info("db_name: %s", db_name)
            logging.info("db_user: %s", db_user)
            
            conn = pm.psql_connection(
                db_name='postgres',
                db_user='postgres',
                db_pass='postgres',
                host='postgresql-headless.default.svc.cluster.local'
                )
        
            cursor = conn.cursor()
            pm.create_database(cursor, db_name=db_name, db_user=db_user, db_pass='12345')
            conn.close()
            logging.info("----------- Creating Database for %s --------------", db_name)
            
        else:
            # The annotations are missing or None
            # Handle this case accordingly
            logging.info("Annotations 'postgresql.db' or 'postgresql.user' are missing or None.")
