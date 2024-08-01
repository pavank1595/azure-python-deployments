from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

# Replace with your Azure subscription ID
subscription_id = "17356c73-f9cc-4e4d-a9be-7a7466852b24"

resource_group_name = 'myResourceGroup'

# Authentication
credential = DefaultAzureCredential()
resource_client = ResourceManagementClient(credential, subscription_id)

async_delete = resource_client.resource_groups.begin_delete(resource_group_name)
    # Wait for the deletion to complete
async_delete.wait()
print(f"Resource group {resource_group_name} has been deleted successfully.")