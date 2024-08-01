from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient


# Replace with your Azure subscription ID
subscription_id = "17356c73-f9cc-4e4d-a9be-7a7466852b24"
location = 'eastus'  # Change to your desired location

# Authentication
credential = DefaultAzureCredential()
resource_client = ResourceManagementClient(credential, subscription_id)

def create_resource_groups(resource_group_names):
    for rg_name in resource_group_names:
        print(f"Creating resource group: {rg_name}")
        resource_group_params = {
            'location': location
        }
        try:
            # Create the resource group
            resource_client.resource_groups.create_or_update(rg_name, resource_group_params)
            print(f"Resource group {rg_name} created successfully.")
        except Exception as e:
            print(f"An error occurred while creating resource group {rg_name}: {e}")

# List of resource group names to create
resource_group_names = ['DEV_RG', 'SIT_RG', 'UAT_RG']

# Create resource groups
create_resource_groups(resource_group_names)
