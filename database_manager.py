from kubernetes import client, config, watch
import logging
# Load Kubernetes configuration from default location
#config.load_kube_config(config_file="/home/user01/.kube/config")
config.load_incluster_config()

# Create a Kubernetes API client
api_instance = client.AppsV1Api()

# Define the namespace and resource type to watch
namespace = 'default'
resource_type = 'deployments'

# Watch for events in the specified namespace and resource type
stream = watch.Watch()

# Iterate through events
i = 0
print("---------------------- Running ------------------")
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
            print("db_name:", db_name)
            print("db_user:", db_user)
        else:
            # The annotations are missing or None
            # Handle this case accordingly
            print("Annotations 'postgresql.db' or 'postgresql.user' are missing or None.")

    i += 1

