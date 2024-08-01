from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

# Replace with your Azure subscription ID
subscription_id = "17356c73-f9cc-4e4d-a9be-7a7466852b24"

resource_group_names_to_delete = ['DEV_RG', 'SIT_RG', 'UAT_RG']

# Authentication
credential = DefaultAzureCredential()
resource_client = ResourceManagementClient(credential, subscription_id)

for rg_name in resource_group_names_to_delete:
        print(f"Deleting resource group: {rg_name}")
        try:
            async_delete = resource_client.resource_groups.begin_delete(rg_name)
            async_delete.wait()
            print(f"Resource group {rg_name} deleted successfully.")
        except HttpResponseError as e:
            print(f"HTTP error occurred while deleting resource group {rg_name}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while deleting resource group {rg_name}: {e}")
