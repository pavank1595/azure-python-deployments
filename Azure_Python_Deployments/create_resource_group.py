from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.core.exceptions import HttpResponseError

# Define your Azure subscription ID and the details for the new resource group
subscription_id = "17356c73-f9cc-4e4d-a9be-7a7466852b24"
resource_group_name = 'dummy_RG'
location = 'north europe'  # e.g., 'eastus', 'westeurope'

resource_group_params = {
  'location': location
}

# Authenticate using DefaultAzureCredential
credential = DefaultAzureCredential()

# Create a Resource Management Client
resource_client = ResourceManagementClient(credential, subscription_id)


# Function to create a resource group
def create_resource_group(subscription_id, resource_group_name, location):
    # Authenticate using DefaultAzureCredential
    credential = DefaultAzureCredential()
    
    # Create a Resource Management Client
    resource_client = ResourceManagementClient(credential, subscription_id)
    
    try:
        # Create or update the resource group
        resource_group_params = {
            'location': location
        }
        response = resource_client.resource_groups.create_or_update(
            resource_group_name,
            resource_group_params
        )
        print(f'Resource group "{resource_group_name}" created successfully in location "{location}".')
        return response
    except HttpResponseError as e:
        print(f'An error occurred: {e.message}')

# Create the resource group
create_resource_group(subscription_id, resource_group_name, location)