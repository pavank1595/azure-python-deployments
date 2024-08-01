from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

# Replace with your Azure subscription ID
subscription_id = "17356c73-f9cc-4e4d-a9be-7a7466852b24"

# Authentication
credential = DefaultAzureCredential()
resource_client = ResourceManagementClient(credential, subscription_id)

resource_groups = resource_client.resource_groups.list()

for rg in resource_groups:
    print(f"Resource Group Name: {rg.name}, Location: {rg.location}")