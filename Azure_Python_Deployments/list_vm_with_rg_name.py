from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient


subscription_id = '17356c73-f9cc-4e4d-a9be-7a7466852b24'

def list_all_vms():
    """Lists all VMs with their resource groups in a subscription."""

    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, subscription_id)
    resource_client = ResourceManagementClient(credential, subscription_id)

    for rg in resource_client.resource_groups.list():
        for vm in compute_client.virtual_machines.list(rg.name):
            print(f"Resource Group: {rg.name}")
            print(f"VM Name: {vm.name}")
            print(f"VM Location: {vm.location}")
            # Add more properties as needed
            print("-" * 30)

list_all_vms()