from kubernetes import client, config, watch
import time
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
for event in stream.stream(api_instance.list_namespaced_deployment, namespace, _request_timeout=60):
    # Check if the event is of type 'ADDED' or 'MODIFIED'
    print("---------------------------- Event ------------------------------------")
    print(event)
    if event['type'] in ['ADDED', 'MODIFIED']:
        deployment = event['object']
        print("---------------------------- deployment -------------------------------")
        print(deployment)
        # Extract annotations from metadata
        annotations = deployment.metadata.annotations
        print("---------------------------- annotation -------------------------------")
        print(annotations)

        # Check if the required annotations exist
#        if 'postgresql.db' in annotations and 'postgresql.user' in annotations:
#            db_name = annotations['postgresql.db']
#            db_user = annotations['postgresql.user']

            # Perform your logic to create the PostgreSQL database here
#            print(f"Creating PostgreSQL database: {db_name}, User: {db_user}")
    else:
        print("Nothing")

